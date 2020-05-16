import numpy as np
import total_loads as tls
from functions import *
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
print('=======================================================')
print('Start buckling computations')



Mx = np.max(np.abs(tls.bending_moment_export))  #[Nm]

'''
For buckling computaitons assume the cross section to be rectangular, with a width of 0.5*c_root and a height of 80% of 
the airfoil max thickness
'''
t_start = 0.0005
sweep = np.deg2rad(sweep)
x = tls.x
step = tls.step
h = 0.5 * c_root
a = 0.8 * 0.2 * c_root
Ixx_start = t_start * h * (a**2) / 3

C = 4  ## based on BCs
E = E*10e5
v = 0.33  # Poisson ratio
Ixx = Ixx_start
n_stiff = 0
t = t_start
A_stiff = 0.015 * 2 * 0.0015
stiff_mass = A_stiff * 1.5 / np.cos(sweep) * 2700
y = a/2
running = True
t_s = []
n_s = []
masses = []
sigmas = []
sigmas_cr = []
index = 0
while running:
    Ixx = t * h * (a ** 2) / 3 + 2 * n_stiff * A_stiff * ( a / 2 )**2
    sigma = Mx * y / Ixx
    print('Normal stress: ',sigma / 10e5, 'MPa')
    b = h/(1 + n_stiff)
    sigma_cr = C * (np.pi**2 * E)/(12 * (1 - v**2)) * ( t / b )**2
    print('Critical stress: ', sigma_cr / 10e5, 'MPa')

    if sigma_cr < sigma:
        t = t + 0.0001
        print('<', t)
        index = 0


    elif sigma_cr > sigma:
        index = index + 1
        chords = findchord(x)
        root_perimeter = 1.596  # [m], perimeter of root airfoil
        skin_perimeters = root_perimeter * chords / c_root
        skin_area = np.trapz(skin_perimeters, dx=step)  # [m2]
        skin_mass = skin_area * t * 1550
        tot_mass = skin_mass + 2 * n_stiff * stiff_mass
        masses.append(tot_mass)
        t_s.append(t)
        n_s.append(n_stiff)
        sigmas.append(sigma)
        sigmas_cr.append(sigma_cr)
        t = t_start
        n_stiff = n_stiff + 1
        print('>')
        if index == 3:
            running = False




    else:
        print('Axial stress is lower than critical stress, no optimisaiton is required')
        print('t = ', t, '; Number of stiffeners = ', n_stiff)
        running = False

plt.scatter(n_s, masses)
plt.show()