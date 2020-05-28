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

debug = False

print('=========== INITIALIZING CROSS SECTION COMPUTATIONS ===========')
if debug:
    print('*************** DEBUG MODE IS ON ***************')
print('Coordinate system origin is at the leading edge of the airfoil')
print('X-axis is pointing towards the TE and Z-axis is pointing up')
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


### create array of points to compute airfoil shape
airfoil_points = np.array([airfoil_points_x, airfoil_points_z])
airfoil_points = airfoil_points.T * par.c_r
### airfoil chord from data points is not exactly 1 unit, but slightly more, so we have to fix the scaling
scaling = par.c_r / (np.max(airfoil_points[:,0]) - np.min(airfoil_points[:,0]))
airfoil_points = airfoil_points * scaling
### points for v&v
if debug:
    mesh = 150    #set to 150
    ## increase number of nodes to check that section properties converge to a single value when number of nodes is indeed increased
    ### define dummy wing box 1.2 meters wide, 1m tall, 0.5mm in thickness
    airfoil_points_x1 = np.zeros(mesh) -0.2
    airfoil_points_x2 = np.linspace(-0.2,1, mesh)
    airfoil_points_x3 = np.ones(mesh)
    airfoil_points_x4 = np.flip(airfoil_points_x2)

    airfoil_points_z1 = np.linspace(-0.5, 0.5, mesh)
    airfoil_points_z2 = 0.5 * np.ones(mesh)
    airfoil_points_z3 = np.flip(airfoil_points_z1)
    airfoil_points_z4 = -airfoil_points_z2

    airfoil_points_x = np.hstack([airfoil_points_x1, airfoil_points_x2, airfoil_points_x3, airfoil_points_x4])
    airfoil_points_z = np.hstack([airfoil_points_z1, airfoil_points_z2, airfoil_points_z3, airfoil_points_z4])
    airfoil_points = np.array([airfoil_points_x, airfoil_points_z]).T
    print(airfoil_points.shape)
##########
### compute center point of each skin segment
airfoil_midpoints_x = (airfoil_points[:,0] + np.roll(airfoil_points[:,0],-1))/2
airfoil_midpoints_z = (airfoil_points[:,1] + np.roll(airfoil_points[:,1],-1))/2
airfoil_midpoints = np.vstack([airfoil_midpoints_x, airfoil_midpoints_z]).T
### compute skin segments length
rolled_points_x = np.roll(airfoil_points[:,0], -1)
rolled_points_z = np.roll(airfoil_points[:,1], -1)
mesh_length = np.sqrt((rolled_points_x - airfoil_points[:,0])**2 + (rolled_points_z - airfoil_points[:,1])**2)
skin_per = np.sum(mesh_length)  ## [m] used to validate what has been done so far, as the perimeter of the skin was computed on CATiA


###### VALIDATE CODE ######
# mesh_length = np.array([0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4, 0.5/4])                                        #for validation
# airfoil_midpoints_z = np.array([0.25, 0.25, 0.25, 0.25, -0.25, -0.25, -0.25, -0.25])                                    #for validation
# airfoil_midpoints_x = np.array([0.5 * 1/8, 0.5 * 3/8, 0.5 * 5/8, 0.5*7/8, 0.5 * 1/8, 0.5 * 3/8, 0.5 * 5/8, 0.5 * 7/8])  #for validation
### validated x_bar, z_bar, Ixx, Izz and Izx match analytical solution of two flat thin plates (t = 0.0005mm) 500mm apart and 500mm long

mesh_area = mesh_length * par.t_sk
# print('computing cross-section properties...')
x_bar = np.sum(mesh_area * airfoil_midpoints_x) / np.sum(mesh_area)
z_bar = np.sum(mesh_area * airfoil_midpoints_z) / np.sum(mesh_area)
print('')
print('x_bar = ', round(x_bar,5), '         m')
print('z_bar = ', round(z_bar,5), '         m')
### Compute second moments of area
Ixx = np.sum(mesh_area * (airfoil_midpoints_z - z_bar)**2)
Izz = np.sum(mesh_area * (airfoil_midpoints_x - x_bar)**2)
Izx = np.sum(mesh_area * (airfoil_midpoints_x * airfoil_midpoints_z))
print('Ixx   = ', "{:3e}".format(Ixx), '    m4')
print('Izz   = ', "{:3e}".format(Izz), '    m4')
print('Izx   = ', "{:3e}".format(Izx), '    m4')

x_sc, z_sc = f.get_shear_center(airfoil_points, airfoil_midpoints, Ixx, Izz, Izx, x_bar, z_bar, skin_per, mesh_length)

plt.plot(airfoil_points_x, airfoil_points_z)
plt.scatter([x_sc], [z_sc])
plt.show()




