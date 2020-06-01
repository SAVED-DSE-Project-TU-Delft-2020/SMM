### import packages
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import scipy.interpolate as sp_interpolate
import timeit
from matplotlib.collections import LineCollection
import seaborn as sns
sns.set()

### import files
import functions as f
import parameters as par
import gather_points
import compute_boom_areas
import define_spars
import Compute_CS as CS

def Load_CS(mesh, debug, c_len, plotting, save_csfig, showplot):
    print('=========== INITIALIZING CROSS SECTION COMPUTATIONS ===========')
    if debug:
        print('*************** DEBUG MODE IS ON ***************')

    airfoil_points_x, airfoil_points_z = gather_points.gatherpoints(mesh, debug)
    airfoil_points_x = airfoil_points_x * c_len
    airfoil_points_z = airfoil_points_z * c_len
    main_spar_loc = par.main_spar_loc * c_len
    aft_spar_loc = par.aft_spar_loc * c_len
    main_spar_t = par.mainspar_cap_t
    main_spar_w = par.mainspar_cap_l
    aft_spar_t = par.aftspar_cap_t
    aft_spar_w = par.aftspar_cap_l
    main_spar_A = main_spar_t * main_spar_w
    aft_spar_A = aft_spar_t * aft_spar_w


    airfoil_points_x = define_spars.cut_cs(airfoil_points_x, main_spar_loc, aft_spar_loc, debug)


    cs_areasloc_x, cs_areasloc_z, cs_areas_size, mesh_len = compute_boom_areas.boomareas(airfoil_points_x, airfoil_points_z, mesh, par.t_sk, main_spar_A, aft_spar_A, main_spar_loc, aft_spar_loc, debug)
    x_bar, z_bar = CS.compute_centroid(cs_areasloc_x, cs_areasloc_z, cs_areas_size)
    print('x_bar = ', round(x_bar, 5), '         m')
    print('z_bar = ', round(z_bar, 5), '         m')
    Ixx, Izz, Izx = CS.compute_SMOA(cs_areasloc_x, cs_areasloc_z, cs_areas_size, x_bar, z_bar)
    print('Ixx   = ', "{:3e}".format(Ixx), '    m4')
    print('Izz   = ', "{:3e}".format(Izz), '    m4')
    print('Izx   = ', "{:3e}".format(Izx), '    m4')

    mesh_perimeter = np.cumsum(mesh_len)
    skin_per = mesh_perimeter[-1]
    x_sc, z_sc = f.compute_sc(airfoil_points_x, airfoil_points_z, cs_areasloc_x, cs_areasloc_z, Ixx, Izz, Izx, x_bar, z_bar, skin_per,
               mesh_len, cs_areas_size)

    if plotting:
        plt.clf()
        # plt.figure(figsize=(9, 5))
        ax = plt.gca()
        # sets the ratio to 5
        ax.set_aspect(1)
        plt.plot(airfoil_points_x, airfoil_points_z, label='Cross section', color='r')
        # plt.plot(np.linspace(0,c_loc, 150), np.zeros(150))
        plt.scatter([x_sc], [z_sc], label = 'Shear center', color = 'g')
        plt.scatter([x_bar], [z_bar], label = 'Centroid', color = 'b', marker = '*')
        plt.legend(loc='upper right', prop={'size': 6})
        if save_csfig:
            plt.savefig('C:\\Users\\marco\\OneDrive\\Documents\\TU Delft\\BSc\\Year 3\\DSE\\Detailed Design\\Plots\\CS_Plots\\cross_section_' + str(round(c_len,4)) + 'c.pdf',dpi=600)
        if showplot:
            plt.show()

    return x_bar, z_bar, Ixx, Izz, Izx, x_sc, z_sc, airfoil_points_x, airfoil_points_z, cs_areasloc_x, cs_areasloc_z, cs_areas_size, mesh_len