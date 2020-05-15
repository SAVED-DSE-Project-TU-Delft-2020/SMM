'''
Author: Marco Desiderio

This program computes strucutral requirements following handling and loads.
The drone is modeled as a distributed weight normalised over the spanwise area distribution.
The drone is supported at both wing tips by simple supports (no moments).
Drone shall not reflect more than 20mm and should be able to support 3 times its own weight

'''


from functions import *
import numpy as np
import loadcases as lcs
import matplotlib.pyplot as plt
import total_loads as tls
print('=======================================================')
print('Start handling loads computations')
plotting = False
n = 2.5
step = lcs.step  #[m]
x = lcs.x       #[m]
y_distribution = tls.y_distribution         #[m]
load_distribution = lcs.load_distribution*n*9.81  #[N]
span = lcs.span                     #[m]
mass = np.trapz(load_distribution,span)/9.81  #just make a sanity check
print('MTOM =',mass/n,'kg')

Ixx_req, bending_moment, shear, vz,dvdz, bending_export = solve_distributed_2pointbending(load_distribution, span, step, 80, sigma_y, E)
Ixx_req = Ixx_req*10e11    #[mm4]
b_cs = 0.5*findchord(x)*1000  #[mm]
b_cs = np.hstack([np.flip(b_cs), b_cs])  #[mm]
# b_cs = np.mean(b_cs)*np.ones(b_cs.shape)
## slice b_cs
b_cs = b_cs[2:-2]
a = y_distribution*1000         #[mm]
t = 3*Ixx_req/(b_cs*a**2)       #[mm]
Ixx = b_cs*t*a**2/3             #[mm4]
if np.max(t)>0.5:
    volume = ((np.max(b_cs) + np.min(b_cs))*lcs.b*1000 + (np.max(y_distribution) + np.min(y_distribution))*lcs.b*1000000)*np.max(t) # [mm3]
else:
    t = 0.5
    volume = ((np.max(b_cs) + np.min(b_cs)) * lcs.b * 1000 + (np.max(y_distribution) + np.min(y_distribution)) * lcs.b * 1000000) * t  # [mm3]
mass = volume*0.0027 # [g]
### add extra mass to account for additional skin panels
mass = mass + 2700*0.0005*2*lcs.S*1000

print('Mass of the strucutre is :',mass, 'g')
Ixx = b_cs*t*a**2/3             #[mm4]
max_normal_stress = bending_moment*1000*y_distribution*1000/Ixx
Ixx = b_cs*t*a**2/3/10e11 #[m4]
b_cs = b_cs/1000        #[m]
shear_export = shear
shear = shear[2:-2]     #[N]
half_cs_centroid = (b_cs*y_distribution + 2*y_distribution*y_distribution/2)/(b_cs + 2*y_distribution)      #[m]
Q = (b_cs*y_distribution + 2*y_distribution*y_distribution/2)*t/1000                                        #[m3]`
tau = (shear*Q)/(Ixx*t/1000)/10e5           #[MPa]

print('Max handling bending stress: ', np.max(np.abs(max_normal_stress)), 'MPa')
print('Max handling shear stress: ', np.max(tau), 'MPa')



if plotting:
    plt.plot(span[2:-2],tau)
    plt.show()


