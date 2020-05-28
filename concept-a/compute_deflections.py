import buckling_computations_v2 as buck
import numpy as np
import total_loads as tls
import matplotlib.pyplot as plt
from parameters import *
import scipy.integrate as sp_int
from  functions import *

Mx = tls.bending_moment_export
t = 0.0006
n_stiff = 2
A_stiff = buck.A_stiff
ax = buck.ax
cx = buck.cx
yx = buck.yx
t_spar = 0.001
NA_loc = (n_stiff * A_stiff * ax) / (n_stiff * A_stiff + cx * t * 2 + yx * t * 2)
Ixx1 = t * np.max(cx) * (np.max(ax) - NA_loc) ** 2 + t * np.max(cx) * (np.max(ax) + NA_loc) ** 2
Ixx2 = t_spar * np.max(yx) ** 3 / 12 * 2
Ixx3 = 2 * t_spar * np.max(yx) * NA_loc ** 2
Ixx4 = n_stiff * A_stiff * (np.max(ax) - NA_loc) ** 2
# print(Ixx1, Ixx2, Ixx3, Ixx4)
Ixx = Ixx1 + Ixx2 + Ixx3 + Ixx4
Ixx = stack_arrays(Ixx)

x = tls.x
span = np.hstack([np.flip(-x), x])
E = buck.E
print(span)
d2v_dz2 = Mx / E / Ixx

dv_dz = sp_int.cumtrapz(d2v_dz2, span, initial=0)
dv_dz = dv_dz - np.median(dv_dz)
vz = sp_int.cumtrapz(dv_dz, span, initial=0)  ## [mm]

plt.plot(span, vz*1000)
plt.show()
