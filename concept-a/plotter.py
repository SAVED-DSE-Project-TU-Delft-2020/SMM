import matplotlib.pyplot as plt
from matplotlib.axes import *
import loadcases as lcs
import Lift_distribution as lift
import numpy as np
import total_loads as tls
import handling_loads as hls
import VTOL_loads as VTOL

import seaborn as sns
sns.set()

lift_distribution = lift.lift_distr
span = lcs.span
load = lcs.load_distribution
bending_moment_maneouv = tls.bending_moment_export
shear_maneouv = tls.shear_export
handling_shear = hls.shear_export
handling_bending = hls.bending_export
shear_VTOL = VTOL.shear_export
bending_VTOL = VTOL.bending_moment_export


xplot = span
yplot1 = bending_moment_maneouv
yplot2 = handling_bending
yplot3 = bending_VTOL

tableau20 = [(255, 87, 87), (255, 158, 0), (87, 255, 249), (0, 0, 0),
             (255, 33, 33), (255, 192, 33), (244, 255, 33), (64, 255, 175),
             (225, 107, 255), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)
#
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
xticks = np.arange(-1.5, 1.6, 0.25)
#yticks = np.arange(np.min(yplot1), np.max(yplot1) , (np.max(yplot1) - np.min(yplot1)/10))
plt.xticks(xticks, fontsize=10)
# plt.yticks(yticks, fontsize=10)
plt.yticks(fontsize=10)
##Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)

##Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
plt.rcParams.update({'font.size': 9})
plt.xlabel('Wingspan location [m]')
plt.ylabel('Internal bending moment [Nm]')
plt.xlim((-1.5, 1.5))
plt.plot(xplot, yplot1, label = 'Flight loads', color=tableau20[4], marker = '1', markersize = 6, markevery = 10)  #colors : 4
plt.plot(xplot, yplot2, label = 'Handling and landing loads', color=tableau20[1], marker='.', markersize=6, markevery = 10)
plt.plot(xplot, yplot3, label = 'VTOL loads', color=tableau20[3], marker='v', markersize=3, markevery = 10)
#plt.plot(shift_wbf, weights_wbf, label='Load window pass. from back', color=tableau20[2], marker='3', markersize=9)
plt.legend()
plt.savefig('C:\\Users\\marco\\OneDrive\\Documents\\TU Delft\\BSc\\Year 3\\DSE\\Deliverables\\Midtem report\\Plots and figures\\bending_tot_vs_span.pdf', dpi = 600)
plt.show()