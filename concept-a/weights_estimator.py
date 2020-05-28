import total_loads as tls
import loadcases as lcs
from functions import *
print('=======================================================')
print('Start weights computations')
x = tls.x
step = tls.step
t = 0.001                             #[m], minimum manufacturable thickness for alu
b_cross_sec = 0.5 * findchord(x)                     #[m]
b_cross_sec = np.hstack([np.flip(b_cross_sec), b_cross_sec])     #[m]
y_distribution = np.flip(np.linspace(0.04 / 2, 0.170 / 2, computenum(0,b / 2,step))) ## [m]root thickness of 120mm and tip thickness of 40mm
y_distribution = np.hstack([np.flip(y_distribution), y_distribution])   #[m]
a_cross_sec = 2*y_distribution                #[m]

#compute mass of wing box, assume it is made of aluminium
wing_box_mass = 2700 * ( 4 * t * (np.min(b_cross_sec) + np.max(b_cross_sec)) * b / 2 / 2 + 4 * t * (np.min(a_cross_sec) + np.max(a_cross_sec)) * b / 2 / 2 )
wing_box_mass = 2700 * ( 4 * t * (np.min(a_cross_sec) + np.max(a_cross_sec)) * b / 2 / 2 )  ### do not account twice for the chord-wise thickness, else skin is just a dead mass

print('Wing-box mass is: ', round(wing_box_mass,3), 'kg')
#### compute mass of skin, assume median of density of selected composites
chords = findchord(x)
root_perimeter = 1.596          #[m], perimeter of root airfoil
t = 0.0005
skin_perimeters = root_perimeter*chords/c_root
skin_area = np.trapz(skin_perimeters, dx = step) * 2  #[m2]for 2 half wings
skin_mass = skin_area*t*1550

print('Skin mass is: ', round(skin_mass,3), 'kg')
### compute mass of the ribs, assume a total of 16 ribs + a central one, material is aluminium and thickness is 1.5mm
ribs_number = 16
ribs_spacing = np.linspace(0, 1.5, ribs_number//2 + 2)[1:-1]    #spanwise location of ribs
ribs_chord = findchord(ribs_spacing)   #[m]
ribs_thickness = 0.20 * ribs_chord  #t/c = 20%
ribs_areas = 0.7 * ribs_chord * ribs_thickness   # from CATIA it was measured that airfoil cs-area is 70% of rectangle enclosing it
ribs_areas = np.sum(0.5 * ribs_areas)                  #50% of rib area will be hollow - we are not civil engineers
ribs_mass = 2 * ribs_areas * 0.0015 * 2700 + c_root * 0.20 * c_root * 0.0015 * 0.7 * 0.5 * 2700

print('Ribs mass is: ', round(ribs_mass,3), 'kg')

## compute mass of payload bay. Materials are foam for insulation (4mm on each face) and PP moulding compound for external shell (2mm on each face)

##external shell dimensions
t_shell = 0.002                         #[m]
side_1 = 0.116 - t_shell / 2            #[m]
side_2 = 0.278 - t_shell / 2            #[m]
side_3 = 0.295 - t_shell / 2            #[m]
rho_shell = 1550                        #[kg/m3]
A_shell = 2 * side_1 * side_2 + 2 * side_2 * side_3 + 2 * side_1 * side_3
mass_shell = t_shell * A_shell * rho_shell
print('Thermoplastic shell mass is: ', round(mass_shell,3), 'kg')

## foam dimensions
t_foam = 0.008          #[m]
side_1 = 0.114          #[m]
side_2 = 0.276 - 2 * t_foam          #[m]
side_3 = 0.293 - 2 * t_foam          #[m]
A_foam = 2 * side_1 * side_2 + 2 * side_2 * side_3 + 2 * side_3 * side_1
mass_foam = t_foam * A_foam * 205
print('Thermoplastic foam mass is: ', round(mass_foam,3), 'kg')





tot_mass = wing_box_mass + skin_mass + ribs_mass + mass_foam + mass_shell

print('Total strucutal mass is: ', round(tot_mass,3), 'kg')

