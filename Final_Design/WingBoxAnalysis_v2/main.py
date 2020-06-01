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
import internal_loads
import compute_normalstress

debug = False
plotting = False
showplot = False
save_csfig = False
start_timer = timeit.default_timer()
mesh = 200


c_lens = np.linspace(par.c_t, par.c_r, par.N)
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
i = 0
for c_len in c_lens:

    x_bar_temp, z_bar_temp, Ixx_temp, Izz_temp, Izx_temp, x_sc_temp, z_sc_temp, x_temp, z_temp, cs_areasloc_x_temp, \
    cs_areasloc_z_temp, cs_areas_size_temp, mesh_len_temp = Load_CS.Load_CS(mesh, debug, c_len, plotting, save_csfig, showplot)
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
    i = i + 1

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


del x_bar_temp, z_bar_temp, Ixx_temp, Izz_temp, Izx_temp, x_sc_temp, z_sc_temp, x_temp, z_temp
### gather internal loads
Mx = internal_loads.Mx_array
Mz = internal_loads.Mz_array
Sx = internal_loads.Sx_array
Sz = internal_loads.Sz_array
### missing torque due to pitching moment


sigma_yy_arr = np.zeros(2 * mesh)
for i in range(par.N):
    i = int(i)
    sigma_yy_temp = f.get_bending_stresses(Mx[i], Mz[i], Ixx_arr[i], Izz_arr[i], Izx_arr[i], x_arr[i,:], z_arr[i,:], x_bar_arr[i], z_bar_arr[i])
    sigma_yy_arr = np.vstack((sigma_yy_arr, sigma_yy_temp))
    line_coordinates = np.cumsum(mesh_len_arr[i,:])
    q_pureshear = compute_pureshear.compute_pureshearflow(Sx[i], Sz[i], Ixx_arr[i], Izz_arr[i], Izx_arr[i], cs_areas_size_arr[i,:],
                                                          cs_areasloc_x_arr[i,:], cs_areasloc_z_arr[i,:], x_bar_arr[i], z_bar_arr[i], line_coordinates, line_coordinates[-1])

sigma_yy_arr = sigma_yy_arr[1:,:]

del sigma_yy_temp
# print(Mx)








##############################################################################################################################################
#### PLOTTING STUFF
location = -1
sigma_yy_loc = sigma_yy_arr[location,:]/10e5

x = x_arr[location,:]
print(x_sc_arr[location])
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
norm = plt.Normalize(sigma_yy_loc.min(), sigma_yy_loc.max())
# norm = plt.Normalize(sigma_vm.min(), sigma_vm.max())
# norm = plt.Normalize(tau_xy_loc.min(), tau_xy_loc.max())
# lc = LineCollection(segments, cmap='RdYlBu', norm=norm)
lc = LineCollection(segments, cmap='RdYlBu_r', norm=norm)
# Set the values used for colormapping
lc.set_array(sigma_yy_loc)
# lc.set_array(sigma_vm)
# lc.set_array(tau_xy_loc)
lc.set_linewidth(3)
line = axs.add_collection(lc)
fig.colorbar(line, ax=axs, label = '$\sigma_{vm}$ [$MPa$]', orientation = 'horizontal', ticks = np.round(np.linspace(sigma_yy_loc.min(), sigma_yy_loc.max(), 15), 2))
plt.xlabel('x [$m$]')
plt.ylabel('z [$m$]')
plt.title('$\sigma_{yy}$ distribution along the airfoil, y = ' + str(location) + 'm')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.scatter(x_sc_arr[location], z_sc_arr[location], marker='*', label = 'Shear center')
# plt.scatter(x_ac_arr[location], z_ac_arr[location], label = 'Aerodynamic center')
plt.scatter(x_bar_arr[location], z_bar_arr[location], label = 'Centroid', marker='1')
axs.set_xlim(x.min() - 0.05, x.max() + 0.05)
axs.set_ylim(y.min() - 0.05, y.max() + 0.05)
plt.legend()
# plt.savefig('test.pdf')
plt.show()

