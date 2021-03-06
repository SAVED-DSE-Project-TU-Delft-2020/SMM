"""
Author: Marco Desiderio
This file loads airfoil points from excel and computes centroid location, second moment of area and shear center location.

Limitations: this program is guaranteed to work with single-cell beams only. Multicell features still need to be implemented
V&V: This code was validates by giving as inputs points from a standard rectangular cross section
the shear center computations present minimal discrepancies which are related to discretisation error. When the number of nodes is increased
the shear center locations converg to the real value, which proves that indeed the inaccuracies are due to discretisation.
A second validation procedure consisted into giving the code the coordinates of a NACA0012 airfoil. The shear center z-location was correcly computed to be in the
symmetry axis
"""
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt
from openpyxl import load_workbook
import parameters as par
import functions as f

def compute_CS_props(c_loc, airfoil_points_x, airfoil_points_z, debug, plotcs, plotshow, plotsavefig, mainspar_A, aftspar_A):
    print('=========== INITIALIZING CROSS SECTION COMPUTATIONS ===========')
    if debug:
        print('*************** DEBUG MODE IS ON ***************')
    ### create array of points to compute airfoil shape
    #### As sometimes the origin does not coincide with the leading edge, we shift the airfoil to achieve this
    airfoil_points_x = np.array([airfoil_points_x])[0]
    airfoil_points_z = np.array([airfoil_points_z])[0]
    airfoil_points_x = airfoil_points_x - airfoil_points_x[np.argmin(airfoil_points_x)]
    airfoil_points_z = airfoil_points_z - airfoil_points_z[np.argmin(airfoil_points_x)]
    airfoil_points = np.array([airfoil_points_x, airfoil_points_z]).T

    ### airfoil chord from data points is not exactly 1 unit, but can be slightly different, so we have to normalise this
    scaling = 1 / (np.max(airfoil_points[:,0]) - np.min(airfoil_points[:,0]))

    airfoil_points = airfoil_points * c_loc * scaling
    ### Redefine x and z coordinates according to scaling
    airfoil_points_x = airfoil_points[:,0]
    airfoil_points_z = airfoil_points[:,1]
    ### points for v&v
    if debug:
        mesh = 150    #set to 150
        ## increase number of nodes to check that section properties converge to a single value when number of nodes is indeed increased

        # airfoil_points_x1 = np.linspace(0, 0.5, mesh)
        # airfoil_points_x2 = np.linspace(0.5, 1, mesh)
        # airfoil_points_x3 = np.linspace(1, 0, mesh)
        # airfoil_points_z1 = np.linspace(0, 0.8, mesh)
        # airfoil_points_z2 = np.linspace(0.8, 0, mesh)
        # airfoil_points_z3 = np.zeros(mesh)
        # airfoil_points_x = np.hstack([airfoil_points_x1, airfoil_points_x2, airfoil_points_x3])
        # airfoil_points_z = np.hstack([airfoil_points_z1, airfoil_points_z2, airfoil_points_z3])
        # airfoil_points = np.array([airfoil_points_x, airfoil_points_z]).T
        airfoil_points_x1 = np.linspace(0, 1.5, 1500)
        airfoil_points_x2 = np.linspace(1.5, 0.9, 600)
        airfoil_points_x3 = np.linspace(0.9, 1.5, 600)
        airfoil_points_x4 = np.linspace(1.5, 0 ,1500)
        airfoil_points_z1 = np.linspace(0, 0.8, 1500)
        airfoil_points_z2 = np.linspace(0.8,0, 600)
        airfoil_points_z3 = np.linspace(0, - 0.8, 600)
        airfoil_points_z4 = np.linspace(- 0.8,0, 1500)

        airfoil_points_x = np.hstack([airfoil_points_x1, airfoil_points_x2, airfoil_points_x3, airfoil_points_x4])
        airfoil_points_z = np.hstack([airfoil_points_z1, airfoil_points_z2, airfoil_points_z3, airfoil_points_z4])
        airfoil_points = np.array([airfoil_points_x, airfoil_points_z]).T
        print(airfoil_points.shape)
    ##########
    ### compute center point of each skin segment
    airfoil_midpoints_x = (airfoil_points[:,0] + np.roll(airfoil_points[:,0],-1))/2
    airfoil_midpoints_z = (airfoil_points[:,1] + np.roll(airfoil_points[:,1],-1))/2
    airfoil_midpoints = np.vstack([airfoil_midpoints_x, airfoil_midpoints_z]).T
    ### compute skin segments length and skin perimeter
    skin_per, mesh_length = f.get_skin_per(airfoil_points)
    #print(skin_per)## [m] used to validate what has been done so far, as the perimeter of the skin was computed on CATiA

    A_enclosed = abs(np.trapz(airfoil_points_x, airfoil_points_z))



    ###### VALIDATE CODE ######
    # mesh_length = np.array([0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4])                                        #for validation
    # airfoil_midpoints_z = np.array([0.25, 0.25, 0.25, 0.25, -0.25, -0.25, -0.25, -0.25])                                    #for validation
    # airfoil_midpoints_x = np.array([0.5 * 1/8, 0.5 * 3/8, 0.5 * 5/8, 0.5*7/8, 0.5 * 1/8, 0.5 * 3/8, 0.5 * 5/8, 0.5 * 7/8])  #for validation
    ### validated x_bar, z_bar, Ixx, Izz and Izx match analytical solution of two flat thin plates (t = 0.0005mm) 500mm apart and 500mm long
    #### compute x and z spar caps locations

    main_spar_upperz = np.max(airfoil_points_z[airfoil_points_x == 0])
    main_spar_lowerz = np.min(airfoil_points_z[airfoil_points_x == 0])
    aft_spar_upperz = np.max(airfoil_points_z[airfoil_points_x == np.max(airfoil_points_x)])
    aft_spar_lowerz = np.min(airfoil_points_z[airfoil_points_x == np.max(airfoil_points_x)])

    mesh_area = mesh_length * par.t_sk
    # print('computing cross-section properties...')
    x_bar = (np.sum(mesh_area * airfoil_midpoints_x) + 2 * aftspar_A * np.max(airfoil_points_x) ) / (np.sum(mesh_area) + 2 * mainspar_A + 2 * aftspar_A)
    z_bar = (np.sum(mesh_area * airfoil_midpoints_z) + mainspar_A * (main_spar_lowerz + main_spar_upperz) + aftspar_A * (aft_spar_lowerz + aft_spar_upperz)) / (np.sum(mesh_area)
                                                                                                                                                                 + 2 * mainspar_A + 2 * aftspar_A)
    print('')
    print('c_loc = ', round(c_loc,5), '         m')
    print('x_bar = ', round(x_bar,5), '         m')
    print('z_bar = ', round(z_bar,5), '         m')
    print('A_enclosed = ', "{:3e}".format(A_enclosed), 'm2')
    ### Compute second moments of area
    Ixx = np.sum(mesh_area * (airfoil_midpoints_z - z_bar)**2)
    Izz = np.sum(mesh_area * (airfoil_midpoints_x - x_bar)**2)
    Izx = np.sum(mesh_area * ((airfoil_midpoints_x - z_bar) * (airfoil_midpoints_z - z_bar)))
    print('Ixx   = ', "{:3e}".format(Ixx), '    m4')
    print('Izz   = ', "{:3e}".format(Izz), '    m4')
    print('Izx   = ', "{:3e}".format(Izx), '    m4')

    x_sc, z_sc = f.get_shear_center(airfoil_points, airfoil_midpoints, Ixx, Izz, Izx, x_bar, z_bar, skin_per, mesh_length)
    if plotcs:
        plt.clf()
        plt.figure(figsize=(9, 5))
        ax = plt.gca()
        # sets the ratio to 5
        ax.set_aspect(1)
        plt.plot(airfoil_points_x, airfoil_points_z, label = 'Cross section', color = 'r')
        # plt.plot(np.linspace(0,c_loc, 150), np.zeros(150))
        plt.scatter([x_sc], [z_sc], label = 'Shear center', color = 'g')
        plt.scatter([x_bar], [z_bar], label = 'Centroid', color = 'b', marker = '*')
        plt.legend(loc = 'upper right', prop={'size': 6})
        if plotsavefig:
            plt.savefig(
                'C:\\Users\\marco\\OneDrive\\Documents\\TU Delft\\BSc\\Year 3\\DSE\\Detailed Design\\Plots\\CS_Plots\\cross_section_' + str(round(c_loc,4)) + 'c.pdf',dpi=600)
        if plotshow:
            plt.show()
    print('=========== CROSS SECTION COMPUTATIONS COMPLETED ===========')


    return x_bar, z_bar, Ixx, Izz, Izx, x_sc, z_sc, A_enclosed, airfoil_points_x, airfoil_points_z, mesh_length




