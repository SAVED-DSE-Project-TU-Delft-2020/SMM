import scipy.integrate as sp_int
import numpy as np
import functions as f
import parameters as par
import matplotlib.pyplot as plt


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def find_nearestval(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def compute_ac(c_loc, cspoints_x, cspoints_z):
    x_ac = 0.25 * c_loc
    z_ac_upper = cspoints_z[cspoints_x == f.find_nearestval(cspoints_x, x_ac)]
    z_ac = (z_ac_upper[0] + z_ac_upper[1]) / 2
    return x_ac, z_ac

def findchord(c_root, y, h):
    '''
    :param y: spanwise location
    :return: cord length at location y
    h is the length of the triangle having its base at c_root and both sides on the sides of the trapezoid
    '''
    c_i = c_root*(1-y/h)

    return c_i

def computenum(start, stop, step):
    '''
    Computes the number of elements of which a segment is divided into given a delta-x
    :param start: start of the segment
    :param stop: stop of the segment
    :param step: delta-x required
    :return: number of elements to use in np.linspace
    '''

    num = int((stop - start)/step)+1
    return num

def findarea(y1, y2, c_r, h):
    '''
    :param y1: spanwise location of chord 1
    :param y2: spanwise location of chord 2
    :return: wing surface between chord 1 and chord 2
    '''
    c1 = findchord(c_r, y1, h)
    c2 = findchord(c_r, y2, h)
    A = trapezarea(c1, c2, abs(y1-y2))
    return A

def trapezarea(c1, c2, h):
    '''
    :param c1: long basis
    :param c2: short basis
    :param h: height
    :return: area of trapezoid
    '''
    return (c1 + c2)*h/2
def get_skin_per(points_x, points_z):
    rolled_points_x = np.roll(points_x, -1)
    rolled_points_z = np.roll(points_z, -1)
    mesh_length = np.sqrt((rolled_points_x - points_x)**2 + (rolled_points_z - points_z)**2)
    skin_per = np.sum(mesh_length)
    return skin_per, mesh_length

def compute_qb(Vx, Vz, Ixx, Izz, Izx, boom_areas, cs_points_x, cs_points_z, x_bar, z_bar):
    x_locs = cs_points_x - x_bar
    z_locs = cs_points_z - z_bar
    qb = - (Vz * Izz - Vx * Izx) / (Ixx * Izz - Izx**2) * (np.cumsum(boom_areas * z_locs)) - (Vx * Ixx - Vz * Izx) / (Ixx * Izz - Izx**2) * (np.cumsum(boom_areas * x_locs))

    return qb
def compute_q0(qb, line_coordinates, skin_perimeter):
    """
    :param qb: Open section shear flow (array)
    :param line_coordinates: Coordinates of the line along you are gonna integrate (array)
    :param skin_perimeter: Length of perimeter along which you are performing the integration
    :return: q0 - Closed section basic shear flow
    """
    q0 = - (sp_int.trapz(qb, line_coordinates))/skin_perimeter
    return q0
def compute_sc(cs_points_x, cs_points_z, cs_midpoints_x, cs_midpoints_z, Ixx, Izz, Izx, x_bar, z_bar, skin_per, mesh_length, boom_areas):
    print('... computing shear center locations ...')
    x = cs_midpoints_x #- x_bar
    z = cs_midpoints_z #- z_bar
    t = par.t_sk
    line_coordinates = np.cumsum(mesh_length)

    ##the start of this coordinate system is at the leading edge. Then the integration continues along the upper surface and comes back
    ##through the lower surface.

    ########################################################################################################################
    ############################### COMPUTE X_SC ###########################################################################
    Sx = 0
    Sz = 1

    qb = compute_qb(Sx, Sz, Ixx, Izz, Izx, boom_areas, cs_midpoints_x, cs_midpoints_z, x_bar, z_bar)
    q0 = compute_q0(qb, line_coordinates, skin_per)
    qs = qb + q0
    qs = qs[:-1]
    airfoil_points_x_rolled = np.roll(cs_points_x,-1)
    airfoil_points_z_rolled = np.roll(cs_points_z, -1)
    x_vectors_base = airfoil_points_x_rolled - cs_points_x
    z_vectors_base = airfoil_points_z_rolled - cs_points_z
    alpha_vect = np.arctan2(z_vectors_base, x_vectors_base)[:-1]
    x_vectors = x_vectors_base[:-1]
    z_vectors = z_vectors_base[:-1]
    shear_magnitudes = np.sqrt(x_vectors**2 + z_vectors**2)*qs
    x_arm = cs_midpoints_x[:-1]
    z_arm = cs_midpoints_z[:-1]
    alpha_arm = np.arctan2(z_arm,x_arm)
    alpha_arm = alpha_arm
    theta = alpha_arm + (np.pi - alpha_vect)

    arms = np.sqrt(x_arm**2 + z_arm**2)
    moments = shear_magnitudes * arms * np.sin(theta)
    x_sc = np.sum(moments)
    print('x_sc = ',"{:2e}".format(x_sc), ' m')

    Sx = 1
    Sz = 0

    qb = compute_qb(Sx, Sz, Ixx, Izz, Izx, boom_areas, cs_midpoints_x, cs_midpoints_z, x_bar, z_bar)
    q0 = compute_q0(qb, line_coordinates, skin_per)
    qs = qb + q0
    qs = qs[:-1]
    airfoil_points_x_rolled = np.roll(cs_points_x,-1)
    airfoil_points_z_rolled = np.roll(cs_points_z, -1)
    x_vectors_base = airfoil_points_x_rolled - cs_points_x
    z_vectors_base = airfoil_points_z_rolled - cs_points_z
    alpha_vect = np.arctan2(z_vectors_base, x_vectors_base)[:-1]
    x_vectors = x_vectors_base[:-1]
    z_vectors = z_vectors_base[:-1]
    shear_magnitudes = np.sqrt(x_vectors**2 + z_vectors**2)*qs
    x_arm = cs_midpoints_x[:-1]
    z_arm = cs_midpoints_z[:-1]
    alpha_arm = np.arctan2(z_arm,x_arm)
    alpha_arm = alpha_arm
    theta = alpha_arm + (np.pi - alpha_vect)

    arms = np.sqrt(x_arm**2 + z_arm**2)
    moments = - shear_magnitudes * arms * np.sin(theta)
    z_sc = np.sum(moments)
    print('z_sc = ',"{:2e}".format(z_sc), ' m')

    return x_sc, z_sc

def get_bending_stresses(Mx, Mz, Ixx, Izz, Izx, x, z, x_bar, z_bar):
    """
    This script takes Cross section properties and bending moments as inputs and returns a normal stress distribution
    This function was validated by comparison with analytical value
    :param Mx: Bending moment x
    :param Mz: Bending moment z
    :param Ixx: SMOAxx
    :param Izz: SMOAzz
    :param Izx: Product moment of area
    :param x: x locations
    :param z: z locations
    :param x_bar: x centroid
    :param z_bar: z centroid
    :return:
    """
    x = x - x_bar
    z = z - z_bar
    part_1 = (Mz * Ixx - Mx * Izx) * x
    part_2 = (Mx * Izz - Mz * Izx) * z
    part_3 = (Ixx * Izz - Izx**2)
    sigma_y = (part_1 + part_2) / part_3

    return sigma_y





