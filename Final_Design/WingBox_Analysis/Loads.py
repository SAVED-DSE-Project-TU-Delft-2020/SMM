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

y_locs = np.array([y_locs])[0][:35]
dL_dy = np.array([dL_dy])[0][:35]

y_locs = sp_interpolate.


L = sp_integrate.trapz(dL_dy, y_locs) * 2
print('Lift = ', L, 'N')

plt.plot(y_locs[:35], dL_dy[:35])
plt.show()