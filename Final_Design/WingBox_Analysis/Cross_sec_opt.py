"""
Author: Marco Desiderio

... insert description ...

"""
import numpy as np
from openpyxl import load_workbook
import Load_CS as CS
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.interpolate as sp_interpolate
sns.set()


wb = load_workbook(filename = r'CAL4014L_Points.xlsx')
sheet = wb.worksheets[0]
# print('creating mesh...')
#print(sheet['A2'].value) # D18
row_count = sheet.max_row                   #count number of rows
airfoil_points_x = []
airfoil_points_z = []
for i in range(2, row_count + 1):
    x_col = 'A'
    z_col = 'B'
    row_number = str(i)
    point_x_loc = sheet[x_col + row_number].value
    point_z_loc = sheet[z_col + row_number].value
    airfoil_points_x.append(point_x_loc)
    airfoil_points_z.append(point_z_loc)
del row_number, point_x_loc, point_z_loc

row_count = row_count - 1

debug = False
plotcs = False
plotshow = True
plotsavefig = False


mesh = 500


c_loc = 0.760

n_iter = 20
main_spar_locs = np.linspace(0, 0.25, n_iter)
main_spar_locs = np.ndarray.tolist(main_spar_locs)
aft_spar_loc = 0.75
airfoil_per = 1.543689436179347
spar_cap_l = 0.040
spar_cap_t = 0.001
spar_cap_A = spar_cap_l * spar_cap_t
Ixxs = np.empty(1)
locs = np.empty(1)
for loc in main_spar_locs:
    airfoil_points_x_arr = np.array([airfoil_points_x])
    airfoil_points_z_arr = np.array([airfoil_points_z])[0].T
    airfoil_points_x_arr[airfoil_points_x_arr < loc] = loc
    airfoil_points_x_arr[airfoil_points_x_arr > aft_spar_loc] = aft_spar_loc
    airfoil_points_x_ite = np.ndarray.tolist(airfoil_points_x_arr)[0]
    points_idx = np.where(airfoil_points_x_arr == loc)[1]
    indices = np.empty(1)
    for i in points_idx:
        print(i)
        indices = np.append(indices, i)
    indices = np.ndarray.astype(indices[1:], int)
    print(indices)
    c_loc_ite = c_loc * (1 - (1 - aft_spar_loc) - loc)
    x_bar, z_bar, Ixx, Izz, Izx, x_sc, z_sc, A_enclosed, airfoil_points_x_loc, airfoil_points_z_loc, mesh_length = CS.compute_CS_props(c_loc_ite, airfoil_points_x_ite, airfoil_points_z, debug, plotcs, plotshow, plotsavefig)
    print(airfoil_points_z_arr.shape)
    z_up_idx = indices[0]
    z_low_idx = indices[-1]
    print(z_up_idx, z_low_idx)
    Ixx = Ixx*10e11 + spar_cap_A# * ((z_up - z_bar)**2 + (z_low - z_bar)**2)
    Ixxs = np.append(Ixxs, Ixx)
    locs = np.append(locs, loc)

locs = locs[1:]
Ixxs = Ixxs[1:]

plt.xlabel('Main spar location as a % of chord [-]')
plt.ylabel('$I_{xx}$ [$m^4$]')
plt.title('Variation of second moment of area with different main spar locations')
plt.plot(locs, Ixxs)
# plt.plot(locs, 0.95 * Ixxs[0] * np.ones(locs.shape[0]))
plt.show()
