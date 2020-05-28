"""
Author: Marco Desiderio
This file computes the loads acting over the wing. Lift distribution is an input from the Aerodynamics department and
the weight distribution is estimated in a similar fashion as in the midterm report.

"""
import numpy as np
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import scipy.integrate as sp_integrate
import scipy.interpolate as sp_interpolate
import parameters as par

print('=========== GENERATING LOAD CASES ===========')

wb = load_workbook(filename = r'testdata.xlsx')
sheet = wb.worksheets[0]
row_count = sheet.max_row                   #count number of rows
y_locs = []
dL_dy = []
for i in range(2, row_count + 1):
    locs_col = 'B'
    lift_col = 'C'
    row_number = str(i)
    point_y_locs = sheet[locs_col + row_number].value
    point_dL_dy_loc = sheet[lift_col + row_number].value
    y_locs.append(point_y_locs)
    dL_dy.append(point_dL_dy_loc)
###### MODIFY THIS WHEN WE GET NEW DATA ######
y_locs = np.array([y_locs])[0][:35]
dL_dy = np.array([dL_dy])[0][:35]

y_locs = np.hstack([[0], y_locs])
dL_dy = np.hstack([[dL_dy[0]], dL_dy])
#################################################

dL_dy_new = sp_interpolate.interp1d(y_locs, dL_dy)

y_mesh = np.linspace(0, par.b/2, par.N * par.segment_mesh)

L_y = sp_integrate.cumtrapz(dL_dy_new(y_mesh), y_mesh, initial=0)
M_y = sp_integrate.cumtrapz(L_y, y_mesh, initial=0)

indexes = np.linspace(par.segment_mesh,par.segment_mesh * par.N, par.N)
indexes = np.ndarray.tolist(indexes)

Sz_array = np.array([])
Mx_array = np.array([])
for i in indexes:
    i = int(i)
    Sz_array = np.append(Sz_array, L_y[i-1])
    Mx_array = np.append(Mx_array, M_y[i-1])


# plt.plot(y_mesh, M_y)
# plt.show()