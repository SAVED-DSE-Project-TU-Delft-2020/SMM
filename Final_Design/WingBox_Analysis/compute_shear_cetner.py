"""
Author: Marco Desiderio
This code computes the shear center of the airfoil
Limitations: this program is guaranteed to work with single-cell beams only. Multicell features still need to be implemented
V&V: This code was validates by giving as inputs points from a standard rectangular cross section
the shear center computations present minimal discrepancies which are related to discretisation error. When the number of nodes is increased
the shear center locations converg to the real value, which proves that indeed the inaccuracies are due to discretisation.
"""

def get_shear_center(airfoil_points, airfoil_midpoints, Ixx, Izz, Izx, x_bar, z_bar, skin_per, mesh_length):

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
