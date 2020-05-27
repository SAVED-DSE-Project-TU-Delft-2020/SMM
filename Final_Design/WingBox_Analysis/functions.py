import scipy.integrate as sp_int

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