import numpy as np
from parameters import *
import scipy.integrate as sp_int
b,S,c_root,c_tip, taper, sweep, c, E, G, sigma_y, tau_s, MTOM, MPAY, MBAT, OEM = get_parameters(Parameters())

print('Taper ratio is: ', round(taper,4))
print('Tip chord is: ', round(c_tip,4))
def findchord(y):
    '''
    :param y: spanwise location
    :return: cord length at location y
    c is the length of the triangle having its base at c_root and both sides on the sides of the trapezoid
    '''
    c_i = c_root*(1-y/c)

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

def trapezarea(c1, c2, h):
    '''
    :param c1: long basis
    :param c2: short basis
    :param h: height
    :return: area of trapezoid
    '''
    return (c1 + c2)*h/2

def findarea(x1, x2):
    '''
    :param x1: spanwise location of chord 1
    :param x2: spanwise location of chord 2
    :return: wing surface between chord 1 and chord 2
    '''
    c1 = findchord(x1)
    c2 = findchord(x2)
    A = trapezarea(c1, c2, abs(x1-x2))
    return A

def extrapolate_linear(x0, x1, y0, y1, x_bar):
    '''
    Extrapolate value using linear interpolation between two values
    :param x0: x-loc of point 0
    :param x1: x-loc of point 1
    :param y0: y-loc of point 0
    :param y1: y-loc of point 1
    :param x_bar: x-loc of point of which we want to know the y coordinate
    :return: y-coordinate of point x_bar
    '''
    return (x_bar-x0)*(y1-y0)/(x1-x0) + y0


def solve_distributed_2pointbending(load_distribution, span, step,maxcompliance, sigma_y, E):
    '''
    :param load_distribution: an arbitrary distributed load
    :param span: points of x-coordinates about the beam
    :param step: step of integration (delta-x)
    :param maxcompliance: maximum allowed compliance
    :return: required Ixx given stress and compliance constraints, internal bending moments and shear forces, rotations and deflecitons of the beam
    the function assumes a beam which is simply supported at both ends
    '''
    shear = sp_int.cumtrapz(load_distribution, span, initial=0)
    shear = shear - np.median(shear)
    bending_moment = sp_int.cumtrapz(shear, span, initial=0)  # [Nm]
    print('Max abs shear: ', np.max(np.abs(shear)), 'N')
    print('Max abs bending moment: ', np.max(np.abs(bending_moment)), 'Nm')

    y_distribution = np.flip(np.linspace(0.03 / 2, 0.075 / 2, computenum(0, b / 2,step)))  ## [m]root thickness of 164mm and tip thickness of 30mm
    y_distribution = np.hstack([np.flip(y_distribution), y_distribution])  # [m]

    sigma_y = sigma_y/2  # [MPa]
    E = E

    bending_moment = bending_moment[2:-2]
    bending_moment = (bending_moment + np.flip(bending_moment)) / 2
    y_distribution = y_distribution[2:-2]
    span = span[2:-2]

    iterating = True
    i = 0
    Ixx_req = abs((bending_moment*y_distribution/(sigma_y*10e5))) # in m4
    while iterating:
        ## measure compliance

        d2v_dz2 = bending_moment/(E*10e5)/Ixx_req


        dv_dz = sp_int.cumtrapz(d2v_dz2, span, initial=0)
        dv_dz = dv_dz - np.median(dv_dz)
        vz = sp_int.cumtrapz(dv_dz,span, initial=0)*1000 ## [mm]

        if np.max(np.absolute(vz)) > maxcompliance:
            i = i + 1
            Ixx_req = 1.05*Ixx_req
        else:
            iterating = False

    return Ixx_req, bending_moment, shear, vz, dv_dz


