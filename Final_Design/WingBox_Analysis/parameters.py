"""
Author: Marco Desiderio
Parameters file for the wing box analysis
"""
import numpy as np
print('=========== LOADING SAVED PARAMETERS ===========')
### Cross-seciton parameters
t_sk = 0.0005           #[m]
t_sp = 0.0010           #[m]

### Wing geometry parameters

b = 3                   #[m]
S = 1.3                 #[m2]
c_r = 0.760             #[m]
c_t = 2 * S / b - c_r   #[m]
sweep_025 = 0 * np.pi / 180  #[deg]

### System paramters
MTOM = 17.50            #[kg]

print('Wingspan is:     ', b, '       m')
print('Wing surface is: ', S, '     m2')
print('Root chord is:   ', c_r, '    m')
print('Tip chord is:    ', round(c_t,4), '  m')
print('MTOM is:         ', MTOM,    '    kg')
