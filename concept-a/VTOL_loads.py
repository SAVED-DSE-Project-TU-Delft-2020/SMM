'''
Author: Marco Desiderio

This program computes strucutral requirements following VTOL loads for the 4 rotors configuration.
The drone is modeled as a distributed weight normalised over the spanwise area distribution.
The drone is supported at the middle of both half-wing by a propeller (simple support).
Drone shall not reflect more than 20mm and should be able to support 1.5 times its own weight

'''


from functions import *
import numpy as np
import scipy.integrate as sp_int
import loadcases as lcs
import matplotlib.pyplot as plt
import total_loads as tls


print('=======================================================')
print('Start VTOL loads computations')

plotting = True


load_distribution = lcs.load_distribution  *1.56 * 9.81
step = lcs.step
span = lcs.span
sigma_y = lcs.sigma_y  #[MPa]
y_distribution = tls.y_distribution  #[m]
E = lcs.E    #[MPa]
x = lcs.x    #[MPa]

loads = np.ones(2) * 16.217 * 9.81 * 1.56 / 2           #[N]
points = np.round(np.linspace(0, load_distribution.shape, 3))

points = np.ndarray.tolist(points)
locs = step * np.array(points) - lcs.b / 2
locs = (locs[:-1] + locs[1:]) / 2
locs = np.round((locs +lcs.b / 2) / 0.005).astype(int)
shear_weight = sp_int.cumtrapz(load_distribution, span, initial=0)  # [N]
shear_lift = np.zeros(shear_weight.shape)
locs_list = np.ndarray.tolist(locs)
i = 0
for loc in locs:
    shear_lift[loc[0] - 1:] = shear_lift[loc[0] - 1:] - loads[i]
    i = i + 1

shear = shear_weight + shear_lift       #[N]

bending_moment = sp_int.cumtrapz(shear, span, initial=0) #[Nm]
bending_moment = (bending_moment + np.flip(bending_moment)) / 2
bending_moment = bending_moment - bending_moment[0]
bending_moment = bending_moment[2:-2]   #[Nm]

span = span[2:-2]   #[m]

print('Max abs shear: ', np.max(np.abs(shear)), 'N')
print('Max abs bending moment: ', np.max(np.abs(bending_moment)), 'Nm')

iterating = True
i = 0
Ixx_req = abs((bending_moment * y_distribution/(sigma_y * 10e5))) # in m4
while iterating:
    ## measure compliance

    d2v_dz2 = bending_moment / (E * 10e5) / Ixx_req


    dv_dz = sp_int.cumtrapz(d2v_dz2, span, initial=0)
    dv_dz = dv_dz - np.median(dv_dz)
    vz = sp_int.cumtrapz(dv_dz,span, initial=0) * 1000 ## [mm]

    if np.max(np.absolute(vz)) > 5000:
        i = i + 1
        Ixx_req = 1.05 * Ixx_req
    else:
        iterating = False

Ixx_req = Ixx_req * 10e11                     #[mm4]
b_cs = 0.5 * findchord(x) * 1000                #[mm]
b_cs = np.hstack([np.flip(b_cs), b_cs])
# b_cs = np.mean(b_cs)*np.ones(b_cs.shape)
b_cs = b_cs[2:-2]
a = y_distribution * 1000                 #[mm]
t = 3 * Ixx_req / (b_cs * a ** 2)               #[mm]
Ixx = b_cs * t * a ** 2 / 3                     #[mm4]
if np.max(t)>0.5:
    volume = ((np.max(b_cs) + np.min(b_cs)) * lcs.b * 1000 + (np.max(y_distribution) + np.min(y_distribution)) * lcs.b * 1000000) * np.max(t) # [mm3]
else:
    t = 0.5
    volume = ((np.max(b_cs) + np.min(b_cs)) * lcs.b * 1000 + (np.max(y_distribution) + np.min(y_distribution)) * lcs.b * 1000000) * t  # [mm3]
mass = volume * 0.0027 # [g]
### add extra mass to account for additional skin panels
mass = mass + 2700 * 0.0005 * 2 * lcs.S * 1000
print('Mass of the strucutre is :',mass, 'g')

Ixx = b_cs * t * a ** 2/3         #[mm4]
max_normal_stress = bending_moment * 1000 * y_distribution * 1000 / Ixx
shear = shear[2:-2]
half_cs_centroid = (b_cs * y_distribution + 2 * y_distribution * y_distribution / 2) / (b_cs + 2 * y_distribution)      #[m]
b_cs = b_cs/1000
Q = (b_cs * y_distribution + 2 * y_distribution * y_distribution / 2 ) * t / 1000                                        #[m3]`
Ixx = Ixx/10e11
tau = (shear * Q) / (Ixx * t / 1000) / 10e5           #[MPa]

print('Max handling bending stress: ', np.max(np.abs(max_normal_stress)), 'MPa')
print('Max handling shear stress: ', np.max(tau), 'MPa')
if plotting:
    plt.plot(span,tau)
    plt.show()
