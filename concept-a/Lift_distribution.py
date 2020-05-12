import numpy as np
import loadcases as lcs
from functions import *
import scipy.interpolate
import matplotlib.pyplot as plt

plotting = False
x = lcs.x
#define loading conditions
#From Flying V lift distribution from Palermo
#half-wing is divided into 5 portions (20% spanwise direction)
data = np.array([1.2, 1.2, 0.95, 0.7, 0.6, 0.0])
x_locs = (lcs.b/2)*np.array([.0, .2, .4, .6, .8, 1.])

interpolate_liftdistrib = scipy.interpolate.interp1d(x_locs, data)
lift_distr = interpolate_liftdistrib(x)
dx = lcs.step
lift = np.trapz(lift_distr, x)
lift_distr = (lcs.MTOM/lift)*lift_distr/2

lift_distr = np.hstack([np.flip(lift_distr), lift_distr])  #[kg/m]
span = lcs.span


if plotting:
    plt.plot(span, lift_distr)
    plt.show()