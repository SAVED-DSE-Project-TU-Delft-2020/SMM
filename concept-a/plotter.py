import matplotlib.pyplot as plt
from matplotlib.axes import *
import loadcases as lcs
import Lift_distribution as lift
import numpy as np
import total_loads as tls
import handling_loads as hls

import seaborn as sns
sns.set()

lift_distribution = lift.lift_distr
span = lcs.span
load = lcs.load_distribution
bending_moment_maneouv = tls.bending_moment_export
shear = tls.shear_export
handling_shear = hls.shear_export
handling_bending = hls.bending_export


xplot = span
yplot = handling_shear

tableau20 = [(255, 87, 87), (137, 255, 87), (87, 255, 249), (0, 0, 0),
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
yticks = np.arange(np.min(yplot), np.max(yplot) , (np.max(yplot) - np.min(yplot)/10))
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
plt.ylabel('Internal shear force [N]')
plt.xlim((-1.5, 1.5))
plt.plot(xplot, yplot, color=tableau20[0])  #colors : 4

plt.savefig('C:\\Users\\marco\\OneDrive\\Documents\\TU Delft\\BSc\\Year 3\\DSE\\Deliverables\\Midtem report\\Plots and figures\\shear_handl_vs_span.pdf', dpi = 600)
plt.show()