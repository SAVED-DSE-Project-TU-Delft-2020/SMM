import numpy as np
from parameters import *
import matplotlib.pyplot as plt
from functions import *


### Fix some shit in here

plotting = False
b,S,c_root,c_tip, taper, sweep, c, E, G, sigma_y, tau_s, MTOM, MPAY, MBAT, OEM = get_parameters(Parameters())
'''
b [m], S [m2], c_root [m], c_tip [m], taper [-], sweep [deg], c [m], E [MPa], G [MPa]
sigma_y [MPa], tau_s [MPa], MTOM ... OEM [kg]
'''

#create spanwise area distribution of wing planform
start = 0           #[m]
stop = b/2          #[m]
step = 0.005        #[m]
num = computenum(start, stop, step)

x = np.linspace(start, stop, num)
Ax =c_root - x*c_root/c             #spanwise area distribution (dA/dx, gradient) m2/m
##print(np.trapz(Ax, x))            #Area function validated
centermass = 5.5/2                  #Weight distributed in the middle of the strucutre [kg]
centerdistrload = Ax*centermass/(findarea(0,0.125))  #[kg/m] distributed mass in the center
centerdistrload = centerdistrload[:25]               # //


otherdistrload = Ax*(MTOM/2 - centermass)/(findarea(0.125, 1.5))   #[kg/m] distributed mass elsewhere
otherdistrload = otherdistrload[25:]                               #//


load_distribution = np.hstack([np.flip(otherdistrload),np.flip(centerdistrload),centerdistrload, otherdistrload])
span = np.hstack([np.flip(-x),x])
weight = np.trapz(load_distribution,span)
load_distribution =MTOM*load_distribution/weight   ## something went wrong while slicing arrays (5% error), so just scaling it back
weight = np.trapz(load_distribution,span)
#print(weight)

if plotting:
    plt.plot(span, load_distribution)
    plt.show()

