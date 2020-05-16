'''
Author: Marco Desiderio
This code computed stresses and deflections of the flying wing given flight loads (load factor of 3.8*1.5)
Two different cases are possible: distributed and discretised. Distributed models both life and weight as distributed loads. 
Discretised models the lift as 9 different point loads acting of the frame of the drone. 

The model was validated comparing results with both an online solver and, when this was not possible, it was checked that 
outputs of the internal shear represented reality (jumps at point loads). Calculations regarding Ixx and stresses were also performed by hand
'''

import loadcases as lcs
import Lift_distribution as lift
from functions import *
import matplotlib.pyplot as plt
import scipy.integrate as sp_int
from math import radians
print('=======================================================')
print('Start aerodynamic loads computations')
span = lcs.span
step = lcs.step
x = lcs.x


case = 'distributed'  #distributed or discretised
plot = False
max_lf = 3.8*1.5
lift_distr = lift.lift_distr*9.81*max_lf   #[N/m]
load_distribution = lcs.load_distribution*9.81*max_lf  #[N/m]



if case == 'discretised':



    points = np.round(np.linspace(0, load_distribution.shape, 10))

    points = np.ndarray.tolist(points)

    start = 0
    loads = []
    for point in points[1:]:
        stop = int(point[0]-1)
        load = np.trapz(lift_distr[start:stop+1], span[start:stop+1])
        start = stop
        loads.append(load)

    loads = np.array(loads)    #[N]
    tot_loads = np.sum(loads)  # sanity check, all the loads shall sum up to 16.217*9.81*3.8*1.5
    locs = step*np.array(points) - lcs.b/2
    locs = (locs[:-1] + locs[1:])/2
    locs = np.round((locs+lcs.b/2)/0.005).astype(int)  # spanwise distribution was divided into 9 segments, so each force is acting in the middle of this segment


    shear_weight = sp_int.cumtrapz(load_distribution, span, initial=0) #[N], internal shear due to weight distribution

    shear_lift = np.zeros(shear_weight.shape)
    locs_list = np.ndarray.tolist(locs)
    i = 0
    for loc in locs:
        shear_lift[loc[0]-1:] = shear_lift[loc[0]-1:] - loads[i]
        i = i + 1
    # shear_weight = shear_weight - np.median(shear_weight)
    # shear_lift = shear_lift - np.median(shear_lift)
    shear = shear_weight + shear_lift
elif case == 'distributed':
    load_distribution_tot = (- lift_distr + load_distribution)  #[N/m]
    shear = sp_int.cumtrapz(load_distribution_tot, span, initial=0)
    shear = shear - np.median(shear)

shear_export = shear
bending_moment = sp_int.cumtrapz(shear, span, initial=0) #[Nm]
bending_moment_export = bending_moment
print('Max abs shear: ', np.max(np.abs(shear)), 'N')
print('Max abs bending moment: ', np.max(np.abs(bending_moment)), 'Nm')



y_distribution = np.flip(np.linspace(0.04/2, 0.130/2, computenum(0,lcs.b/2,step))) ## [m]root thickness of 120mm and tip thickness of 40mm
y_distribution_export = y_distribution
y_distribution = np.hstack([np.flip(y_distribution), y_distribution])   #[m]


sigma_y = lcs.sigma_y/2  # [MPa]
E = lcs.E                 #[MPa]
### now slide bending as it is 0 at extremes and thus it would give a required Ixx of 0, however
### this would give an error when bending moment is divided again by Ixx to compute deflections

bending_moment = bending_moment[2:-2]
bending_moment = (bending_moment + np.flip(bending_moment))/2
y_distribution = y_distribution[2:-2]
span = span[2:-2]

iterating = True
i = 0
Ixx_req = abs((bending_moment*y_distribution/(sigma_y*10**6))) # in m4
a = 2*y_distribution*1000                   #[mm]
b_cs = 0.5*findchord(x)*1000                #[mm]
b_cs = np.hstack([np.flip(b_cs), b_cs])     #[mm]
b_cs = b_cs[2:-2]                           #[mm]
'''
while iterating:
    ## measure compliance

    d2v_dz2 = bending_moment/(E*10e5)/Ixx_req


    dv_dz = sp_int.cumtrapz(d2v_dz2, span, initial=0)
    dv_dz = dv_dz - np.median(dv_dz)
    vz = sp_int.cumtrapz(dv_dz,span, initial=0)*1000 ## deflection in [mm]

    if np.max(np.absolute(vz)) > 50000:  ## specify a value for max allowed compliance
        i = i + 1
        Ixx_req = 1.05*Ixx_req
        print('i')
    else:
        iterating = False


Ixx_req = Ixx_req*10e11                     #[mm4]


t = 3*Ixx_req/(b_cs*a**2)                   #[mm]
t_distribution = t
Ixx = b_cs*t*a**2/3                         #[mm4]
if np.max(t)>0.5:
    volume = ((np.max(b_cs) + np.min(b_cs))*lcs.b*1000 + (np.max(y_distribution) + np.min(y_distribution))*lcs.b*1000000)*np.max(t) # [mm3]
else:
    t = 0.5
    volume = ((np.max(b_cs) + np.min(b_cs)) * lcs.b * 1000 + (np.max(y_distribution) + np.min(y_distribution)) * lcs.b * 1000000) * t  # [mm3]
mass = volume*0.0027 # [g]
print('Mass of the box is :',mass, 'g')
### add extra mass to account for additional skin panels (outside load carrying box).
mass = mass + 2700*0.0005*1000*2*(lcs.S - (np.max(b_cs) + np.min(b_cs)) *lcs.b/2 /1000)

print('Mass of the strucutre is :',mass, 'g')

#### Update deflection following new skin thickness
Ixx = b_cs*t*a**2/3/10e11                                       #[m4]
max_normal_stress = bending_moment*y_distribution/Ixx/10e5      #[MPa]
d2v_dz2 = bending_moment / (E * 10e5) / Ixx

dv_dz = sp_int.cumtrapz(d2v_dz2, span, initial=0)
dv_dz = dv_dz - np.median(dv_dz)
vz = sp_int.cumtrapz(dv_dz, span, initial=0) * 1000  ## [mm]
### compute max shear stress
b_cs = b_cs/1000        #[m]
shear = shear[2:-2]     #[N]
half_cs_centroid = (b_cs*y_distribution + 2*y_distribution*y_distribution/2)/(b_cs + 2*y_distribution)      #[m]
Q = (b_cs*y_distribution + 2*y_distribution*y_distribution/2)*t/1000                                        #[m3]`
tau = (shear*Q)/(Ixx*t/1000)/10e5           #[MPa]

#### Make calculaitons for isogrid panel

F = bending_moment/y_distribution/2   ## [N] force trough compression panelloa
'''
## torsion due to sweep
sweep_half = 10
side_span = np.linspace(0, np.tan(radians(sweep_half))*b/2, lcs.num)
side_span_full = stack_arrays(side_span)
lift_distr = np.flip(lift.lift_distr[:lift.lift_distr.shape[0]//2])
torque_distr = lift_distr*side_span
torque = np.flip(sp_int.cumtrapz(np.flip(torque_distr), side_span, initial=0))
# total_troque = np.trapz(torque_distr, side_span)
# print(total_troque)
torque_distr = stack_arrays(torque_distr)[2:-2]
area_distribution = a*b_cs/1000
tau_distribution = torque_distr/(2*area_distribution*0.0005)/10e5

if plot:
    plt.plot(span, tau_distribution)
    plt.show()