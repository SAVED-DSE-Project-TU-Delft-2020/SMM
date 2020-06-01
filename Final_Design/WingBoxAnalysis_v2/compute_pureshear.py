import functions as f
import parameters as par
import numpy as np

def compute_pureshearflow(Vx, Vz, Ixx, Izz, Izx, boom_areas, cs_points_x, cs_points_z, x_bar, z_bar, line_coordinates, skin_perimeter):
    qb = f.compute_qb(Vx, Vz, Ixx, Izz, Izx, boom_areas, cs_points_x, cs_points_z, x_bar, z_bar)
    q0 = f.compute_q0(qb, line_coordinates, skin_perimeter)
    return qb + q0

def compute_sheartorsion(T, Am):
    q = T / (2 * Am)
    return q
def compute_torsion_sc_offset(Sx, Sz, x_sc, z_sc, x_ac, z_ac):
    Sx_arm = np.abs(z_ac - z_sc)
    Sz_arm = np.abs(x_ac - x_sc)
    Ty_Sx = Sx * Sx_arm
    Ty_Sz = Sz * Sz_arm
    Ty = Ty_Sx + Ty_Sz
    return Ty

