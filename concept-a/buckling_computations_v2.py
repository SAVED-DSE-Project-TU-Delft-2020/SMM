'''
Author: Marco Desiderio

This program takes bending moment and basic geometric parameters as inputs and iterates to find the most optimal (lightest)
combination of skin thickness and number of stiffeners.

It outputs max normal stress, critical stress, number of stiffeners for each combination, skin thickness
mass of structure and generated a plot of mass vs number of stiffeners.


'''


import total_loads as tls
import numpy as np
from functions import *
import matplotlib.pyplot as plt
import scipy.interpolate
import seaborn as sns
sns.set()
print('=======================================================')
print('Start buckling computations')


plotting = True
# define constants
E = E*10e5
E = 50000*10e5
v = 0.3
x = tls.x #[m] half wing span
step = tls.step

#define box geometry
cx = findchord(x) / 2 #[m]
yx = tls.y_distribution_export * 2 #[m]
ax = yx / 2
t_start = 0.0005            #[m]
t_spar = 0.001
### we have 8 ribs per half-wing
rib_pitch = 1.5 / 9 #[m]
ribs_idx = np.linspace(0,x.shape, 10)
ribs_idx= np.round(ribs_idx).astype(int)   #index of ribs locations


#bending moment distribution
Mx = tls.bending_moment_export
Mx = Mx[Mx.shape[0]//2:] #slice to get only half-span

#

# Ixx_start = t_start * cx * (yx**2) / 3

Ixx_start = t_start * cx * ax**2 * 2 + t_spar * yx**3 / 12 * 2

sigma_start = Mx * ax / Ixx_start
# critical stress is at the root, as expected
Mx_cr = Mx[0]
Mx_cr = 83.0
print('Root bending moment is:           ', Mx_cr)

n_stiff = 0
t = t_start
A_stiff = 0.015 * 2 * 0.0015
L_stiff = 1.5 / np.cos(np.deg2rad(sweep))

stiff_mass = A_stiff * L_stiff * 2700
running = True
t_s = []
n_s = []
masses = []
sigmas = []
sigmas_cr = []
index = 0
coefficients = np.array([8, 8, 6, 5, 4, 4])
a_bs = np.array([0, 0.45, 0.5, 0.6, 1, 10])
Cs = scipy.interpolate.interp1d(a_bs, coefficients)
Ixxs = []

while running:
    chords = cx * 2
    root_perimeter = 1.596  # [m], perimeter of root airfoil
    skin_perimeters = root_perimeter * chords / c_root
    skin_area = np.trapz(skin_perimeters, dx=step)  # [m2]
    skin_mass = skin_area * t * 1550 * 2
    stiff_tot_mass = 2 * n_stiff * stiff_mass
    tot_mass = skin_mass + stiff_tot_mass
    print('=================== ITERATING ===================')
    print('Number of stringers  =            ', n_stiff)
    print('Skin thickness       =            ', round(t * 1000,3), 'mm')
    print('Skin mass            =            ', round(skin_mass, 3), 'kg')
    print('Stiff mass           =            ', round(stiff_tot_mass, 3), 'kg')
    print('Structural mass      =            ', round(tot_mass,3), 'kg')
    NA_loc = (n_stiff * A_stiff * np.max(ax))/(n_stiff * A_stiff + np.max(cx) * t * 2 + np.max(yx) * t * 2)
    Ixx1 = t * np.max(cx) * (np.max(ax) - NA_loc)**2 + t * np.max(cx) * (np.max(ax) + NA_loc)**2
    Ixx2 = t_spar * np.max(yx)**3 / 12 * 2
    Ixx3 = 2 * t_spar * np.max(yx) * NA_loc**2
    Ixx4 = n_stiff * A_stiff * ( np.max(ax) - NA_loc )**2
    # print(Ixx1, Ixx2, Ixx3, Ixx4)
    Ixx =  Ixx1 + Ixx2 + Ixx3 + Ixx4
    Ixxs.append(Ixx)
    sigma = abs(Mx_cr * np.max(ax) / Ixx)
    # print(Mx_cr, np.max(ax), Ixx)
    print('Normal stress:                   ',round(sigma / 10e5,3), 'MPa')
    b = np.max(cx)/(1 + n_stiff)
    a_b = rib_pitch / b
    print('a/b =                            ', round(a_b,3))
    C = Cs(a_b)
    print('Buckling coefficient = ', C)
    sigma_cr = C * (np.pi**2 * E)/(12 * (1 - v**2)) * ( t / b )**2
    print('Critical stress =                ', round(sigma_cr / 10e5,3), 'MPa')

    if sigma_cr < sigma:
        t = t + 0.0001
        print('Increased thickness; new value = ', round(t * 1000,3), 'mm')
        index = 0


    elif sigma_cr > sigma:
        index = index + 1
        masses.append(tot_mass)
        t_s.append(t)
        n_s.append(n_stiff)
        sigmas.append(sigma)
        sigmas_cr.append(sigma_cr)
        t = t_start
        n_stiff = n_stiff + 1
        print('Increased number of stiffeners; new value = ', n_stiff)
        if index == 3:
            running = False




    else:
        print('Axial stress is lower than critical stress, no optimisaiton is required')
        print('t = ', t, '; Number of stiffeners = ', n_stiff)
        running = False
n_s = np.array(n_s)
masses = np.array(masses)
if plotting:
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
    xticks = np.arange(0, 5, 1)
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
    plt.xlabel('Number of stiffening elements')
    plt.ylabel('Stiffened skin structural mass [kg]')
    print('Lightest stiffened mass is: ', masses[1], 'kg')
    plt.scatter(n_s, masses, label = 'Minimum-skin structural mass', marker='o')
    plt.scatter(n_s[2], masses[2], marker = 'o', s =160, label = 'Design point', facecolor = 'none', edgecolors='r')
    plt.legend()
    plt.savefig('C:\\Users\\marco\\OneDrive\\Documents\\TU Delft\\BSc\\Year 3\\DSE\\Deliverables\\Midtem report\\Plots and figures\\flyingwing_stiffenedmass.pdf', dpi = 600)
    plt.show()