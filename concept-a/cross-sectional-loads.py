'''
Author: Marco Desiderio

This scripts computes the requires Ixx of the frame of the flying wing given a battery load
I.e. battery is mounted (force downwards) and lift is lifting the wing up, so some stiffness is required in order not to deform the airfoil shape
'''

import numpy as np
import scipy.integrate as sp_int
import matplotlib.pyplot as plt
import parameters as p

li_ion_density = 2600 #[kg/m3]

## assume battery takes 50% of chord length and 50% of this thickness
## assume a flat panel in 2 points bending 400x300 mm (chordwise x spanwise)

c = .400
s = .300
t_airfoil = 0.15*c
t_battery = 0.5*t_airfoil

w_battery = 2600*s*t_battery*9.81 #[N/m]
reacts = w_battery*0.5*c/2
## discretise
nodes = 800
z = np.linspace(0,c,nodes)
distributed_load1 = np.zeros(nodes//4)
distributed_load2 = w_battery*np.ones(nodes//2)
distributed_load = np.hstack([distributed_load1, distributed_load2, distributed_load1])

shear_distrload = sp_int.cumtrapz(distributed_load[199:599], z[nodes//2:nodes*3//2], initial=0)
shear_distrload = np.hstack([np.zeros(200), shear_distrload, np.zeros(200)])
shear = np.zeros(z.shape) + reacts
shear = shear - shear_distrload
shear[599:] = shear[599]

bending_moment = sp_int.cumtrapz(shear, z, initial=0)

## assume cross section height of 15mm, with neutral axis in the middle

y_max = 0.0075
sigma_y = p.sigma_y/2

## assume rectangular cs with a 'shape factor' of 0.1 as it will not be rectangular but of a stiffened shape

t_req = (((0.5*bending_moment)*(12/0.03)*(1/sigma_y/10e6))**0.5)*1000





plt.plot(z,bending_moment)
plt.show()
