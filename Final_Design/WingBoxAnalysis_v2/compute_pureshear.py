import functions as f
import parameters as par

def compute_pureshearflow(Vx, Vz, Ixx, Izz, Izx, boom_areas, cs_points_x, cs_points_z, x_bar, z_bar, line_coordinates, skin_perimeter):
    qb = f.compute_qb(Vx, Vz, Ixx, Izz, Izx, boom_areas, cs_points_x, cs_points_z, x_bar, z_bar)
    q0 = f.compute_q0(qb, line_coordinates, skin_perimeter)
    return qb + q0

def compute_sheartorsion(T, Am)
    q = T/(2 * Am)
    return q
