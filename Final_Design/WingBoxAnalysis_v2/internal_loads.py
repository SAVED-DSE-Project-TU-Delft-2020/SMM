import numpy as np
import external_loads
import parameters as par
import scipy.integrate as sp_integrate
import  scipy.interpolate as sp_interpolate
import matplotlib.pyplot as plt
import functions as f
# import sys
# np.set_printoptions(threshold=sys.maxsize)
case = external_loads.case
print('=========== GENERATING INTERNAL LOADS ===========')
print('*********** Case is:', case, '***********')
debug = False
aileron = False



y_mesh = np.linspace(par.b/2, par.PAY_WIDTH/2, par.N * par.segment_mesh)
L_y = - sp_integrate.cumtrapz(external_loads.dL_dy_new(y_mesh), y_mesh, initial=0)       ### LIFT FORCE DISTRIBUTION (shear)
w_final = external_loads.w_final * par.LF
w_final = sp_interpolate.interp1d(external_loads.y, w_final)                     #Loads distribution interpolated
S_y = sp_integrate.cumtrapz(w_final(y_mesh), y_mesh, initial=0)
Mx_y = - sp_integrate.cumtrapz(S_y, y_mesh, initial=0)                  ### BENDING MOMENT DISTRIBUTION

indexes = np.linspace(par.segment_mesh,par.segment_mesh * par.N, par.N)
indexes = np.ndarray.tolist(indexes)

Sz_array = np.array([])
Mx_array = np.array([])

for i in indexes:
    i = int(i)
    Sz_array = np.append(Sz_array, S_y[i-1])
    Mx_array = np.append(Mx_array, Mx_y[i-1])

## change this later once we get the data
D_y = L_y / par.L_D
Sx_y = D_y
e1_index = f.find_nearest(y_mesh, par.e1_loc)
e2_index = f.find_nearest(y_mesh, par.e2_loc)
Sx_y[e1_index:] = Sx_y[e1_index:] - par.T1
Sx_y[e2_index:] = Sx_y[e2_index:] - par.T2

Mz_y = sp_integrate.cumtrapz(Sx_y, y_mesh, initial=0)
Sx_array = np.array([])
Mz_array = np.array([])
Ty_array = np.array([])
### torsion due to pitching moment/sweep/aileron
if aileron:
    Ty = external_loads.Ty_pitchingmoment
else:
    Ty = external_loads.Ty_pitchingmoment/10
for i in indexes:
    i = int(i)
    Sx_array = np.append(Sx_array, D_y[i-1])
    Mz_array = np.append(Mz_array, Mz_y[i-1])
    Ty_array = np.append(Ty_array, Ty[i-1])


if debug:

    plt.xlabel('y [$m$]')
    plt.ylabel('Mx [$Nm$]')
    plt.title('Spanwise bending moment distribution (half-wing)')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
    # plt.plot(np.linspace(0,1.5,10), Ty_array, label = 'Bending moment distribution')
    plt.plot(y_mesh, Mx_y, label = 'Lift distribution')
    # plt.plot(y, w_final, label = 'Total distribution')
    # plt.legend(loc = 'upper right')
    plt.show()