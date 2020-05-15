import numpy as np
import total_loads as tls
from functions import *

print('=======================================================')
print('Start buckling computations')



Mx = np.max(np.abs(tls.bending_moment_export))  #[Nm]

'''
For buckling computaitons assume the cross section to be rectangular, with a width of 0.5*c_root and a height of 80% of 
the airfoil max thickness
'''
t_start = 0.0005
h = 0.5 * c_root
a = 0.8 * 0.2 * c_root
Ixx_start = t_start * b * (a**2) / 3
C = 4  ## based on BCs
E = E*10e5
v = 0.33  # Poisson ratio
running = True
Ixx = Ixx_start
n_stiff = 0
t = t_start
stiffener_unitmass = 0.015 * 0.0015 * 2 * 2700
y = a/2
while running:

    sigma = Mx * y / Ixx
    b = h/(1 + n_stiff)
    sigma_cr = C * (np.pi**2 * E)/(12 * (1 - v**2)) * (t/b)**2

    if sigma_cr < sigma:

     t = np.linspace(0.0005, 0.002, 16)
     t_b = np.sqrt((sigma * (12 * (1 - v**2)))/(C * np.pi**2 * E))
     b_req = t / t_b
     running = False
     print(t, b_req)

    else:
        print('Axial stress is lower than critical stress, no optimisaiton is required')
        running = False

