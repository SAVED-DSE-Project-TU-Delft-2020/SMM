"""
Author: Marco Desiderio
Parameters file for the wing box analysis
"""
import numpy as np
print('=========== LOADING DRONE PARAMETERS ===========')
### Cross-seciton parameters
t_sk = 0.0005           #[m]
t_sp = 0.0010           #[m]

### Wing geometry parameters

b = 3                   #[m]
S = 1.3                 #[m2]
c_r = 0.760             #[m]
c_t = 2 * S / b - c_r   #[m]
taper = c_t / c_r
sweep_025 = 0 * np.pi / 180  #[deg]
h = (b/2) / (1 - taper) #height of triangle having root chord as a base and sides along leading and trailing edges
### System paramters
MTOM = 17.80            #[kg]
L_D = 20
LF = 4 * 0.25

print('Wingspan is:     ', b, '       m')
print('Wing surface is: ', S, '     m2')
print('Root chord is:   ', c_r, '    m')
print('Tip chord is:    ', round(c_t,4), '  m')
print('MTOM is:         ', MTOM,    '    kg')
print('L/D is:          ', L_D)
print('LF is :          ', LF)
### Discretise each half-wing into N segments
N = 100
segment_mesh = 100

### Masses ---- ALL IN KG
###PROP
M_BAT = 2.95
M_ENG = 2.47
###SMM
M_SPARS = 1.38 * 1.15
M_SKINS = 2.21 * 1.15
M_STIFF = 1.14 * 1.15
M_SHELL = 0.91 * 1.15
M_INSUL = 0.44 * 1.15
M_FINS = 0.85 * 1.15
###AI
M_AI = 0.363
###PAYLOAD
M_PAY = 3
### PARACHUTE
M_PARACH = 0.3

##### PAYLOAD BAY DIMENSIONS
PAY_CHORD = 0.295
PAY_WIDTH = 0.268
PAY_HEIGHT = 0.128