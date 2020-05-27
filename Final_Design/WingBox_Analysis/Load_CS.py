'''
Author: Marco Desiderio
This file loads airfoil points from excel and computes centroid location, second moment of area and shear center location.
'''
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt
from openpyxl import load_workbook

### load points from excel
wb = load_workbook(filename = r'NACA35120_Points.xlsx')
sheet = wb.worksheets[0]
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
### create array of points to compute airfoil shape
airfoil_points = np.array([airfoil_points_x, airfoil_points_z])
airfoil_points = airfoil_points.T
### compute center point of each skin segment
airfoil_midpoints_x = (airfoil_points[:,0] + np.roll(airfoil_points[:,0],-1))/2
airfoil_midpoints_z = (airfoil_points[:,1] + np.roll(airfoil_points[:,1],-1))/2
airfoil_midpoints = np.vstack([airfoil_midpoints_x, airfoil_midpoints_z]).T
### compute skin segments length
rolled_points_x = np.roll(airfoil_points[:,0], -1)
rolled_points_z = np.roll(airfoil_points[:,1], -1)
print(rolled_points_x[0], airfoil_points[0,0], rolled_points_z[0], airfoil_points[0,1])
mesh_length = np.sqrt((rolled_points_x - airfoil_points[:,0])**2 + (rolled_points_z - airfoil_points[:,1])**2)
print(mesh_length)