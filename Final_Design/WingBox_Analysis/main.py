"""
Author: Marco Desiderio

This code defines the 3D wing geometry

... complete description ...
"""
import Load_CS as CS
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt
from openpyxl import load_workbook
import parameters as par
import functions as f
import timeit
import Loads

debug = False
plotcs = False
plotshow = False
plotsavefig = False
print('=========== INITIALIZING STRUCTURAL ANALYSIS COMPUTATIONS ===========')
start = timeit.default_timer()
print('Coordinate system origin is located at the leading edge of the airfoil')
print('X-axis is pointing towards the TE and Z-axis is pointing up')
print('The CS origin depends of the input data')
# print('loading workbook...')
### load points from excel
wb = load_workbook(filename = r'NACA35120_Points.xlsx')
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


c_1 = par.c_r
x_bar, z_bar, Ixx, Izz, Izx, x_sc, z_sc, airfoil_points_x_loc, airfoil_points_z_loc = CS.compute_CS_props(c_1, airfoil_points_x, airfoil_points_z, debug, plotcs, plotshow, plotsavefig)

### create chords list
c_locs = np.linspace(par.c_t, par.c_r, 300)
c_locs_list = np.ndarray.tolist(c_locs)
### initialise arrays
x_bar_arr = np.zeros(1)
z_bar_arr = np.zeros(1)
Ixx_arr = np.zeros(1)
Izz_arr = np.zeros(1)
Izx_arr = np.zeros(1)
x_sc_arr = np.zeros(1)
z_sc_arr = np.zeros(1)
airfoil_points_x_arr = np.zeros(airfoil_points_x_loc.shape[0])
airfoil_points_z_arr = np.zeros(airfoil_points_x_loc.shape[0])
for c_loc in c_locs_list:
    x_bar, z_bar, Ixx, Izz, Izx, x_sc, z_sc, airfoil_points_x_loc, airfoil_points_z_loc = CS.compute_CS_props(c_loc,
                                                                                                              airfoil_points_x,
                                                                                                              airfoil_points_z,
                                                                                                              debug,
                                                                                                              plotcs, plotshow, plotsavefig)
    x_bar_arr = np.append(x_bar_arr, x_bar)
    z_bar_arr = np.append(z_bar_arr, z_bar)
    Ixx_arr = np.append(Ixx_arr, Ixx)
    Izz_arr = np.append(Izz_arr, Izz)
    Izx_arr = np.append(Izx_arr, Izx)
    x_sc_arr = np.append(x_sc_arr, x_sc)
    z_sc_arr = np.append(z_sc_arr, z_sc)
    airfoil_points_x_arr = np.vstack((airfoil_points_x_arr, airfoil_points_x_loc))
    airfoil_points_z_arr = np.vstack((airfoil_points_z_arr, airfoil_points_z_loc))

x_bar_arr = x_bar_arr[1:]
z_bar_arr = z_bar_arr[1:]
Ixx_arr = Ixx_arr[1:]
Izz_arr = Izz_arr[1:]
Izx_arr = Izx_arr[1:]
x_sc_arr = x_sc_arr[1:]
z_sc_arr = z_sc_arr[1:]
airfoil_points_x_arr = airfoil_points_x_arr[1:,:]
airfoil_points_z_arr = airfoil_points_z_arr[1:,:]









###time program execution
print('=========== STRUCTURAL ANALYSIS COMPUTATIONS COMPLETED ===========')
stop = timeit.default_timer()
print('Runtime: ', round(stop - start,4)*1000, 'ms')
print('==================================================================')