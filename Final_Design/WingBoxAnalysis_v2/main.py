"""
Author: Marco Desiderio
"""
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
print('=========== INITIALIZING STRUCTURAL ANALYSIS COMPUTATIONS ===========')
print('Running main')
print('Coordinate system origin is located at the leading edge of the airfoil')
print('X-axis is pointing towards the TE and Z-axis is pointing up')
print('The CS origin depends of the input data')
### import packages
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import scipy.interpolate as sp_interpolate
import timeit
from matplotlib.collections import LineCollection
import seaborn as sns
import compute_pureshear
sns.set()

### import files
import functions as f
import parameters as par
import gather_points
import compute_boom_areas
import define_spars
import Compute_CS as CS
import Load_CS
# import CS_opt as Load_CS
import internal_loads
import compute_normalstress
import compute_buckling


debug = False
plotting = False
showplot = False
save_csfig = False
solve = True
stiffeners = True

start_timer = timeit.default_timer()
mesh = 1000


c_lens = np.linspace(par.c_t, par.c_r, par.N)
y_pos = np.linspace(par.b/2, 0, par.N)
c_lens = np.ndarray.tolist(c_lens)
x_bar_arr = np.zeros(0)
z_bar_arr = np.zeros(0)
Ixx_arr = np.zeros(0)
Izz_arr = np.zeros(0)
Izx_arr = np.zeros(0)
x_sc_arr = np.zeros(0)
z_sc_arr = np.zeros(0)
x_arr = np.zeros(2 * mesh)
z_arr = np.zeros(2 * mesh)
cs_areasloc_x_arr = np.zeros(2 * mesh)
cs_areasloc_z_arr = np.zeros(2 * mesh)
cs_areas_size_arr = np.zeros(2 * mesh)
mesh_len_arr = np.zeros(2 * mesh)
mainspar_z_arr = np.zeros(2)
aftspar_z_arr = np.zeros(2)
i = 0
for c_len in c_lens:

    x_bar_temp, z_bar_temp, Ixx_temp, Izz_temp, Izx_temp, x_sc_temp, z_sc_temp, x_temp, z_temp, cs_areasloc_x_temp, \
    cs_areasloc_z_temp, cs_areas_size_temp, mesh_len_temp,mainspar_min_z_temp, mainspar_max_z_temp, aftspar_min_z_temp, \
    aftspar_max_z_temp = Load_CS.Load_CS(mesh, debug, c_len, plotting, save_csfig, showplot, stiffeners)
    x_bar_arr = np.append(x_bar_arr, x_bar_temp)
    z_bar_arr = np.append(z_bar_arr, z_bar_temp)
    Ixx_arr = np.append(Ixx_arr, Ixx_temp)
    Izz_arr = np.append(Izz_arr, Izz_temp)
    Izx_arr = np.append(Izx_arr, Izx_temp)
    x_sc_arr = np.append(x_sc_arr, x_sc_temp)
    z_sc_arr = np.append(z_sc_arr, z_sc_temp)
    x_arr = np.vstack((x_arr, x_temp))
    z_arr = np.vstack((z_arr, z_temp))
    cs_areasloc_x_arr = np.vstack((cs_areasloc_x_arr, cs_areasloc_x_temp))
    cs_areasloc_z_arr = np.vstack((cs_areasloc_z_arr, cs_areasloc_z_temp))
    cs_areas_size_arr = np.vstack((cs_areas_size_arr, cs_areas_size_temp))
    mesh_len_arr = np.vstack((mesh_len_arr, mesh_len_temp))
    mainspar_z_arr = np.vstack((mainspar_z_arr, [mainspar_min_z_temp, mainspar_max_z_temp]))
    aftspar_z_arr = np.vstack((aftspar_z_arr, [aftspar_min_z_temp, aftspar_max_z_temp]))
    i = i + 1
del x_bar_temp, z_bar_temp, Ixx_temp, Izz_temp, Izx_temp, x_sc_temp, z_sc_temp, x_temp, z_temp, cs_areasloc_x_temp
del cs_areasloc_z_temp, cs_areas_size_temp, mesh_len_temp, mainspar_max_z_temp, mainspar_min_z_temp, aftspar_min_z_temp
del aftspar_max_z_temp
# x_bar_arr = x_bar_arr
# print(x_bar_arr[0])
# z_bar_arr = z_bar_arr
# Ixx_arr = Ixx_arr
# Izz_arr = Izz_arr
# Izx_arr = Izx_arr
# x_sc_arr = x_sc_arr
# z_sc_arr = z_sc_arr
x_arr = x_arr[1:,:]
z_arr = z_arr[1:,:]
cs_areasloc_x_arr = cs_areasloc_x_arr[1:,:]
cs_areasloc_z_arr = cs_areasloc_z_arr[1:,:]
cs_areas_size_arr = cs_areas_size_arr[1:,:]
mesh_len_arr = mesh_len_arr[1:,:]
mainspar_z_arr = mainspar_z_arr[1:,:]
aftspar_z_arr = aftspar_z_arr[1:,:]

x_ac_arr = np.zeros(0)
z_ac_arr = np.zeros(0)
for i in range(par.N):
    x_ac_temp, z_ac_temp = f.compute_ac(c_lens[i], x_arr[i,:], z_arr[i,:])
    x_ac_arr = np.append(x_ac_arr, x_ac_temp)
    z_ac_arr = np.append(z_ac_arr, z_ac_temp)
del x_ac_temp, z_ac_temp

if solve:
    ### gather internal loads
    Mx = internal_loads.Mx_array
    Mz = internal_loads.Mz_array
    Sx = internal_loads.Sx_array
    Sz = internal_loads.Sz_array
    ### missing torque due to pitching moment


    sigma_yy_arr = np.zeros(2 * mesh)
    q_tot_arr = np.zeros(2 * mesh)
    line_coordinates_arr = np.zeros(2 * mesh)
    for i in range(par.N):
        i = int(i)
        sigma_yy_temp = f.get_bending_stresses(Mx[i], Mz[i], Ixx_arr[i], Izz_arr[i], Izx_arr[i], x_arr[i,:], z_arr[i,:], x_bar_arr[i], z_bar_arr[i])
        sigma_yy_arr = np.vstack((sigma_yy_arr, sigma_yy_temp))
        line_coordinates = np.cumsum(mesh_len_arr[i,:])
        line_coordinates_arr = np.vstack((line_coordinates_arr, line_coordinates))
        q_pureshear_temp = compute_pureshear.compute_pureshearflow(Sx[i], Sz[i], Ixx_arr[i], Izz_arr[i], Izx_arr[i], cs_areas_size_arr[i,:],
                                                              cs_areasloc_x_arr[i,:], cs_areasloc_z_arr[i,:], x_bar_arr[i], z_bar_arr[i], line_coordinates, line_coordinates[-1])
        q_shearoffset_temp = compute_pureshear.compute_torsion_sc_offset(Sx[i], Sz[i], x_sc_arr[i], z_sc_arr[i], x_ac_arr[i], z_ac_arr[i])
        q_tot_temp = q_pureshear_temp + q_shearoffset_temp
        q_tot_arr = np.vstack((q_tot_arr, q_tot_temp))

    del sigma_yy_temp, q_tot_temp, q_shearoffset_temp, q_pureshear_temp, line_coordinates
    sigma_yy_arr = sigma_yy_arr[1:,:]
    q_tot_arr = q_tot_arr[1:,:]
    line_coordinates_arr = line_coordinates_arr[1:,:]

    tau_xy_arr = q_tot_arr / par.t_sk








    location = -1
    sigma_cr_skin = compute_buckling.compute_axial_buckling(4, 50 * 10e8, 0.33, par.t_sk, line_coordinates_arr[location, :])
    sigma_yy_loc = sigma_yy_arr[location,:]/10e5
    # z_arr_loc = z_arr[location,:]
    # z_mainsparup_real = z_arr_loc[z_arr_loc == f.find_nearestval(z_arr_loc, mainspar_z_arr[location,1])]
    # z_aftsparup_real = z_arr_loc[z_arr_loc == f.find_nearestval(z_arr_loc, aftspar_z_arr[location, 1])]
    # start_buckling = np.where(z_arr_loc == z_mainsparup_real)[0][0]
    # stop_buckling = np.where(z_arr_loc == z_aftsparup_real)[0][0]
    # line_coord = 0
    # iteration = 0
    # for mesh in mesh_len_arr[location, start_buckling:stop_buckling]:
    #     line_coord = line_coord + mesh
    #     sigma_cr_skin_temp = compute_buckling.compute_axial_buckling(4, 50 * 10e8, 0.33, par.t_sk, line_coord)
    #     excess = sigma_cr_skin_temp/10e5 + sigma_yy_loc[start_buckling + iteration]
    #     print(excess)
    #     if excess < 0:
    #         print('placing stiffener')
    #         print('stiffener x-loc: ', x_arr[location, iteration + start_buckling])
    #         print('stiffener z_loc: ', z_arr_loc[iteration + start_buckling])


    ############################################################################################################################################
    ############################################################################################################################################
    #### COMPUTE VON MISES STRESSES ####

    ### for now we define some stresses to be zero, we will change this once we have values

    sigma_excess = sigma_cr_skin/10e5 + sigma_yy_loc
    sigma_excess = np.ma.masked_where(sigma_excess > 0, sigma_excess)
    sigma_xx_loc = sigma_yy_loc * 0
    sigma_zz_loc = sigma_yy_loc * 0
    tau_xy_loc = tau_xy_arr[location, :]/10e5
    tau_yz_loc = sigma_yy_loc * 0
    tau_zx_loc = sigma_yy_loc * 0
    sigma_vm = np.sqrt(((sigma_yy_loc + sigma_xx_loc)**2 + (sigma_yy_loc - sigma_zz_loc)**2 + (sigma_zz_loc - sigma_xx_loc)**2) / 2 + 3 * (tau_xy_loc**2 + tau_yz_loc**2 + tau_zx_loc**2))
    print('=========== STRUCTURAL ANALYSIS COMPUTATIONS COMPLETED ===========')
    ###time program execution
    stop_timer = timeit.default_timer()
    print('Runtime: ', round(stop_timer - start_timer, 3) * 1000, 'ms')
    print('==================================================================')
    ##############################################################################################################################################
    #### PLOTTING STUFF



    x = x_arr[location,:]
    y = z_arr[location,:]
    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    print('Plotting ...')
    fig, axs = plt.subplots(1, 1)
    ax = plt.gca()
    # sets the ratio
    ax.set_aspect(1)
    # Create a continuous norm to map from data points to colors
    # norm = plt.Normalize(sigma_yy_loc.min(), sigma_yy_loc.max())
    # norm = plt.Normalize(sigma_vm.min(), sigma_vm.max())
    # norm = plt.Normalize(tau_xy_loc.min(), tau_xy_loc.max())
    norm = plt.Normalize(sigma_excess.min(), sigma_excess.max())
    # lc = LineCollection(segments, cmap='RdYlBu', norm=norm)
    lc = LineCollection(segments, cmap='RdYlBu_r', norm=norm)
    # Set the values used for colormapping
    # lc.set_array(sigma_yy_loc)
    # lc.set_array(sigma_vm)
    lc.set_array(sigma_excess)
    # lc.set_array(tau_xy_loc)
    lc.set_linewidth(3)
    line = axs.add_collection(lc)
    fig.colorbar(line, ax=axs, label = '$\sigma_{vm}$ [$MPa$]', orientation = 'horizontal')#, ticks = np.round(np.linspace(-5, 5, 14), 2))
    plt.xlabel('x [$m$]')
    plt.ylabel('z [$m$]')
    plt.title('$\sigma_{yy}$ distribution along the airfoil, y = ' + str(y_pos[location]) + 'm')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.scatter(x_sc_arr[location], z_sc_arr[location], marker='*', label = 'Shear center')
    plt.scatter(x_ac_arr[location], z_ac_arr[location], label = 'Aerodynamic center', marker='+')
    plt.scatter(x_bar_arr[location], z_bar_arr[location], label = 'Centroid', marker='1')
    axs.set_xlim(x.min() - 0.05, x.max() + 0.05)
    axs.set_ylim(y.min() - 0.05, y.max() + 0.05)
    plt.legend()
    # plt.savefig('test.pdf')
    plt.show()

