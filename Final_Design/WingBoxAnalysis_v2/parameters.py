"""
Author: Marco Desiderio
Parameters file for the wing box analysis
"""
import numpy as np
print('=========== LOADING DRONE PARAMETERS ===========')
### Cross-seciton parameters
t_sk = 0.000625           #[m]
t_sp = 0.0010           #[m]

### Wing geometry parameters

b = 3                   #[m]
S = 1.318374324                 #[m2]
c_r = 0.6277972969             #[m]
c_t = 2 * S / b - c_r   #[m]
taper = c_t / c_r
sweep_025 = 16 * np.pi / 180  #[deg]
h = (b/2) / (1 - taper) #height of triangle having root chord as a base and sides along leading and trailing edges
### System paramters
MTOM = 17.80            #[kg]
L_D = 22.475262326932008
LF =  3          #4

print('Wingspan is:     ', b, '       m')
print('Wing surface is: ', S, '     m2')
print('Root chord is:   ', round(c_r, 4), '   m')
print('Tip chord is:    ', round(c_t,4), '  m')
print('Taper ratio is:  ', round(taper,3), '   -')
print('MTOM is:         ', MTOM,    '    kg')
print('L/D is:          ', round(L_D,4))
print('LF is :          ', LF)

####### STRUCTURAL PARAMETERS ########
main_spar_loc = 0.0001
aft_spar_loc = 0.999
mainspar_cap_l = 0.00
mainspar_cap_t = 0.00
aftspar_cap_l = 0.020 * 0
aftspar_cap_t = 0.001 * 0
########
# stiffeners_index = np.array([100, 200, 300, 400, 500, 1625, 1800])
# stiffeners_size = np.array([0.000045, 0.000045, 0.000045, 0.000045, 0.000045, 0.000045, 0.000045]) / 1.5
stiffeners_index = np.array([120, 250, 385, 530, 730, 1580, 1780])
stiffeners_size = np.array([0.000045, 0.000045, 0.000045, 0.000045, 0.000045, 0.000045, 0.000045]) / 1.5
### Discretise each half-wing into N segments
N = 10
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

#### ENGINE STUFF
e1_loc = 0.525
e2_loc = 1.050
T1 = 58
T2 = 58