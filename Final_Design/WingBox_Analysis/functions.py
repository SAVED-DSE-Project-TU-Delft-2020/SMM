import scipy.integrate as sp_int
import numpy as np
import functions as f
import parameters as par
import matplotlib.pyplot as plt

def find_qb(Sx, Sz, Ixx, Izz, Izx, line_coordinates, t, x, z):
    """
    This function will compute the open section shear flow given loads
    :param Sx: Shear force in the x direction
    :param Sz: Shear force in the z direction
    :param Ixx: Second moment of area about the x axis
    :param Izz: SMOA about the z axis
    :param Izx: Product moment of area
    :param line_coordinates: Coordinates of the line along you are gonna integrate (array)
    :param t: skin thickness
    :param x: x-coordinates (array)
    :param y: y-coordinates (array)
    :return: shear flow in line coordinates

Function was validated by computing the shear flows of
    """
    qb = - ((Sx * Ixx - Sz * Izx) / (Ixx * Izz - Izx**2)) * (t * sp_int.cumtrapz(x, line_coordinates, initial=0)) - ((Sz * Izz - Sx * Izx) / (Ixx * Izz - Izx**2)) * (t * sp_int.cumtrapz(z, line_coordinates, initial=0))

    return qb

def find_q0(qb, line_coordinates, skin_perimeter):
    """

    :param qb: Open section shear flow (array)
    :param line_coordinates: Coordinates of the line along you are gonna integrate (array)
    :param skin_perimeter: Length of perimeter along which you are performing the integration
    :return: q0 - Closed section basic shear flow
    """
    q0 = - (sp_int.trapz(qb, line_coordinates))/skin_perimeter
    return q0

def get_shear_center(airfoil_points, airfoil_midpoints, Ixx, Izz, Izx, x_bar, z_bar, skin_per, mesh_length):
    """

    :param airfoil_points: array of points defining the geometry of the airfoil
    :param airfoil_midpoints: array of points between the airfoil_points
    :param Ixx: SMOAxx
    :param Izz: SMOAzz
    :param Izx: Product moment of area
    :param x_bar: x-centroid of the cs
    :param z_bar: z-centroid of the cs
    :param skin_per: perimeter of the cross section
    :param mesh_length: length of the mesh
    :return: x and z location of the shear center
    """

    print('... computing shear center locations ...')
    airfoil_points_x = airfoil_points[:,0]
    airfoil_points_z = airfoil_points[:,1]
    x = airfoil_points_x - x_bar
    z = airfoil_points_z - z_bar
    t = par.t_sk
    line_coordinates = np.cumsum(mesh_length)
    ##the start of this coordinate system is at the trailing edge. Then the integration continues along the upper surface and comes back
    ##through the lower surface.

    ########################################################################################################################
    ############################### COMPUTE X_SC ###########################################################################
    Sx = 0
    Sz = 1

    qb = f.find_qb(Sx, Sz, Ixx, Izz, Izx, line_coordinates, t, x, z)
    q0 = f.find_q0(qb, line_coordinates, skin_per)
    qs = qb + q0
    qs = qs[:-1]
    ###################################
    #### Validate script
    # print(qs[525])    ## This shall be 0 or close enough to 0
    # force1 = np.trapz(qs[:150], line_coordinates[:150])
    # force2 = np.trapz(-qs[300:450], line_coordinates[300:450])
    # force = force1 + force2
    ### Script is validates as integral of shear flow in a vertical direction given the input shear force
    ###################################
    ###theta =  alpha_arm + (180 - alpha_vect)

    airfoil_points_x_rolled = np.roll(airfoil_points_x,-1)
    airfoil_points_z_rolled = np.roll(airfoil_points_z, -1)
    x_vectors_base = airfoil_points_x_rolled - airfoil_points_x
    z_vectors_base = airfoil_points_z_rolled - airfoil_points_z
    alpha_vect = np.arctan2(z_vectors_base, x_vectors_base)[:-1]
    x_vectors = x_vectors_base[:-1]
    z_vectors = z_vectors_base[:-1]
    shear_magnitudes = np.sqrt(x_vectors**2 + z_vectors**2)*qs
    x_arm = airfoil_midpoints[:,0][:-1]
    z_arm = airfoil_midpoints[:,1][:-1]
    alpha_arm = np.arctan2(z_arm,x_arm)
    alpha_arm = alpha_arm
    theta = alpha_arm + (np.pi - alpha_vect)

    arms = np.sqrt(x_arm**2 + z_arm**2)
    moments = shear_magnitudes * arms * np.sin(theta)
    x_sc = np.sum(moments)
    print('x_sc = ',"{:2e}".format(x_sc), ' m')


    ########################################################################################################################
    ############################### COMPUTE X_SC ###########################################################################


    Sx = 1
    Sz = 0

    qb = f.find_qb(Sx, Sz, Ixx, Izz, Izx, line_coordinates, t, x, z)
    q0 = f.find_q0(qb, line_coordinates, skin_per)
    qs = qb + q0
    qs = qs[:-1]
    ###################################
    #### Validate script
    # print(qs[525])    ## This shall be 0 or close enough to 0
    # force1 = np.trapz(qs[:150], line_coordinates[:150])
    # force2 = np.trapz(-qs[300:450], line_coordinates[300:450])
    # force = force1 + force2
    ### Script is validates as integral of shear flow in a vertical direction given the input shear force
    ###################################
    ###theta =  alpha_arm + (180 - alpha_vect)

    airfoil_points_x_rolled = np.roll(airfoil_points_x,-1)
    airfoil_points_z_rolled = np.roll(airfoil_points_z, -1)
    x_vectors_base = airfoil_points_x_rolled - airfoil_points_x
    z_vectors_base = airfoil_points_z_rolled - airfoil_points_z
    alpha_vect = np.arctan2(z_vectors_base, x_vectors_base)[:-1]
    x_vectors = x_vectors_base[:-1]
    z_vectors = z_vectors_base[:-1]
    shear_magnitudes = np.sqrt(x_vectors**2 + z_vectors**2)*qs
    x_arm = airfoil_midpoints[:,0][:-1]
    z_arm = airfoil_midpoints[:,1][:-1]
    alpha_arm = np.arctan2(z_arm,x_arm)
    alpha_arm = alpha_arm
    theta = alpha_arm + (np.pi - alpha_vect)

    arms = np.sqrt(x_arm**2 + z_arm**2)
    moments = shear_magnitudes * arms * np.sin(theta)
    z_sc = np.sum(moments)
    print('z_sc = ',"{:2e}".format(z_sc), 'm')


    ###################################
    #### Validate script
    # print(qs[525])    ## This shall be 0 or close enough to 0
    # force1 = np.trapz(qs[:150], line_coordinates[:150])
    # force2 = np.trapz(-qs[300:450], line_coordinates[300:450])
    # force = force1 + force2
    ### Script is validates as integral of shear flow in a vertical direction given the input shear force
    ###################################


    # plt.scatter(airfoil_points[:,0], airfoil_points[:,1])
    # plt.plot(line_coordinates[:-1], qs)
    # plt.show()
    return x_sc, z_sc
