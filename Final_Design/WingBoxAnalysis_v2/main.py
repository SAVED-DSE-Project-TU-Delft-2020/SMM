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
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import scipy.interpolate as sp_interpolate
import scipy.integrate as sp_integrate
import timeit
from matplotlib.collections import LineCollection
import seaborn as sns
import compute_pureshear
from mpl_toolkits.mplot3d import Axes3D
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
showplot = True
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

A_enc = np.zeros(par.N)
for i in range(par.N):
    split_z_temp = np.split(cs_areasloc_z_arr[i,:], 2)
    split_x_temp = np.split(cs_areasloc_x_arr[i,:], 2)
    A_enc_top = sp_integrate.trapz(split_z_temp[0], split_x_temp[0])
    A_enc_low = sp_integrate.trapz(split_z_temp[1], split_x_temp[1])
    A_enc[i] = A_enc_low + A_enc_top
del split_x_temp, split_z_temp, A_enc_low, A_enc_top


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
        T_shearoffset_temp = compute_pureshear.compute_torsion_sc_offset(Sx[i], Sz[i], x_sc_arr[i], z_sc_arr[i], x_ac_arr[i], z_ac_arr[i])
        T_rest_temp = internal_loads.Ty[i]
        T_tot_temp = T_rest_temp + T_shearoffset_temp
        q_tors_temp = compute_pureshear.compute_sheartorsion(T_tot_temp, A_enc[i])
        q_tot_temp = q_pureshear_temp + q_tors_temp
        q_tot_arr = np.vstack((q_tot_arr, q_tot_temp))

    del sigma_yy_temp, q_tot_temp, q_tors_temp, q_pureshear_temp, line_coordinates, i, T_shearoffset_temp, T_rest_temp
    del T_tot_temp
    sigma_yy_arr = sigma_yy_arr[1:,:]
    q_tot_arr = q_tot_arr[1:,:]
    line_coordinates_arr = line_coordinates_arr[1:,:]
    spacing  = 0.050
    rivet_forces = q_tot_arr * spacing
    tau_xy_arr = np.abs(q_tot_arr / par.t_sk)







    for i in range(1):
        location = -1
        sigma_cr_skin = compute_buckling.compute_axial_buckling(4, 50 * 10e8, 0.33, par.t_sk, line_coordinates_arr[location, :])
        sigma_yy_loc = sigma_yy_arr[location,:]

        stiffeners_index = par.stiffeners_index
        stiffeners_index = np.hstack([[0], stiffeners_index[:-2], [1000], stiffeners_index[-2:], [2000]])
        sigma_cr_skin_loc = np.zeros(2 * mesh)
        tau_cr_skin_loc = np.zeros(2 * mesh)
        for index in range(stiffeners_index.shape[0]-1):

            b = np.sum(mesh_len_arr[location,stiffeners_index[index]:stiffeners_index[index + 1]])
            sigma_cr_skin_temp = compute_buckling.compute_axial_buckling(4, 50 * 10e8, 0.33, par.t_sk,b) / 1.5   #USE A SF OF 1.5
            tau_cr_skin_temp = compute_buckling.compute_shear_buckling(5, 50 * 10e8, 0.33, par.t_sk, b) / 1.5
            sigma_cr_skin_loc[stiffeners_index[index]:stiffeners_index[index + 1]] = sigma_cr_skin_temp
            tau_cr_skin_loc[stiffeners_index[index]:stiffeners_index[index + 1]] = tau_cr_skin_temp
            xc_loc = x_arr[location,stiffeners_index[index]] / c_lens[location]
            print('Boom', index,'location is ', round(xc_loc,4), '% of chord')
        del sigma_cr_skin_temp, tau_cr_skin_temp, index,xc_loc






        # sigma_cr_skin_temp = compute_buckling.compute_axial_buckling(4, 50 * 10e8, 0.33, par.t_sk, line_coord)


        ############################################################################################################################################
        ############################################################################################################################################
        #### COMPUTE VON MISES STRESSES ####

        ### for now we define some stresses to be zero, we will change this once we have values
        sigma_yy_loc = sigma_yy_loc/10e5
        tau_xy_loc = tau_xy_arr[location, :] / 10e5
        sigma_cr_skin_loc = sigma_cr_skin_loc/10e5
        tau_cr_skin_loc = tau_cr_skin_loc/10e5
        combined_buckling = - sigma_yy_loc/sigma_cr_skin_loc + (tau_xy_loc/tau_cr_skin_loc)**2
        combined_buckling = np.ma.masked_where(sigma_yy_loc>0, combined_buckling)
        # combined_buckling = np.ma.masked_where(combined_buckling > 1, combined_buckling)
        # combined_buckling = np.ma.masked_where(combined_buckling < 0, combined_buckling)
        # sigma_cr_skin_loc = np.ma.masked_where(sigma_cr_skin_loc > 15, sigma_cr_skin_loc)
        sigma_excess = sigma_cr_skin_loc + sigma_yy_loc
        sigma_excess = np.ma.masked_where(sigma_excess < 0, sigma_excess)
        sigma_xx_loc = sigma_yy_loc * 0
        sigma_zz_loc = sigma_yy_loc * 0

        tau_yz_loc = sigma_yy_loc * 0
        tau_zx_loc = sigma_yy_loc * 0
        sigma_vm = np.sqrt(((sigma_yy_loc + sigma_xx_loc)**2 + (sigma_yy_loc - sigma_zz_loc)**2 + (sigma_zz_loc - sigma_xx_loc)**2) / 2 + 3 * (tau_xy_loc**2 + tau_yz_loc**2 + tau_zx_loc**2))
        print('=========== STRUCTURAL ANALYSIS COMPUTATIONS COMPLETED ===========')
        if stiffeners:
            print('********** STIFFENING MODE WAS ON **********')
        ###time program execution
        stop_timer = timeit.default_timer()
        print('Runtime: ', round(stop_timer - start_timer, 3) * 1000, 'ms')
        print('==================================================================')
        ##############################################################################################################################################
        #### PLOTTING STUFF
        # ax = plt.gca()
        # ax.set_aspect(1)
        # plt.minorticks_on()
        # plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        # plt.xlabel('x [m]')
        # plt.ylabel('y [m]')
        # plt.scatter(cs_areasloc_x_arr[location, :], cs_areasloc_z_arr[location, :],
        #             s=1600000 * cs_areas_size_arr[location, :], color='k', label = 'Boom')
        # plt.legend()
        # plt.savefig('booms.pdf')
        # plt.show()



        x = x_arr[location,:]
        y = z_arr[location,:]
        # Create a set of line segments so that we can color them individually
        # This creates the points as a N x 1 x 2 array so that we can stack points
        # together easily to get the segments. The segments array for line collection
        # needs to be (numlines) x (points per line) x 2 (for x and y)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        print('Plotting ...')
        fig, axs = plt.subplots(1, 1, figsize= (15,5))
        ax = plt.gca()
        # sets the ratio
        # ax.set_aspect(1)
        # Create a continuous norm to map from data points to colors
        # norm = plt.Normalize(sigma_yy_loc.min(), sigma_yy_loc.max())
        # norm = plt.Normalize(sigma_vm.min(), sigma_vm.max())
        # norm = plt.Normalize(tau_xy_loc.min(), tau_xy_loc.max())
        # norm = plt.Normalize(sigma_excess.min(), sigma_excess.max())
        norm = plt.Normalize(combined_buckling.min(), combined_buckling.max())
        # norm = plt.Normalize(sigma_cr_skin_loc.min(), sigma_cr_skin_loc.max())
        # lc = LineCollection(segments, cmap='RdYlBu', norm=norm)
        lc = LineCollection(segments, cmap='RdYlBu_r', norm=norm)
        # Set the values used for colormapping
        # lc.set_array(sigma_yy_loc)
        # lc.set_array(sigma_vm)
        # lc.set_array(sigma_excess)
        # lc.set_array(tau_xy_loc)
        # lc.set_array(sigma_cr_skin_loc)
        lc.set_array(combined_buckling)
        lc.set_linewidth(3)
        line = axs.add_collection(lc)
        # fig.colorbar(line, ax=axs, label = '$\sigma_{VM}$ [$MPa$]', orientation = 'horizontal', ticks = np.round(np.linspace(sigma_vm.min(), sigma_vm.max(), 17), 2))
        fig.colorbar(line, ax=axs, label = 'Interaction curves coefficient [-]', orientation = 'horizontal', ticks = np.round(np.linspace(0,1,17),3))
        # fig.colorbar(line, ax=axs, label='$\sigma_{vm}$ [$MPa$]', orientation='horizontal', ticks = np.round(np.linspace(0,2,20)))
        plt.xlabel('x [$m$]')
        plt.ylabel('z [$m$]')
        plt.title('Interaction curves coefficient distribution along the airfoil [-], y = ' + str(round(y_pos[location],3)) + 'm')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.scatter(x_sc_arr[location], z_sc_arr[location], marker='*', label = 'Shear center')
        plt.scatter(x_ac_arr[location], z_ac_arr[location], label = 'Aerodynamic center', marker='+')
        plt.scatter(x_bar_arr[location], z_bar_arr[location], label = 'Centroid', marker='1')
        plt.scatter(cs_areasloc_x_arr[location, :], cs_areasloc_z_arr[location,:], s = 1600000 * cs_areas_size_arr[location,:],
                    color = 'k', label = 'Booms')
        axs.set_xlim(x.min() - 0.05, x.max() + 0.05)
        axs.set_ylim(y.min() - 0.05, y.max() + 0.05)
        plt.legend()
        plt.savefig('C:\\Users\\marco\\OneDrive\\Documents\\TU Delft\\BSc\\Year 3\\DSE\\Detailed Design\\Plots\\Stresses\\ICC_y=' + str(round(y_pos[location],3)) + '.pdf')


plt.show()