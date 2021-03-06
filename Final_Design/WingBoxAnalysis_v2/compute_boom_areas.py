import numpy as np
import gather_points
import functions as f

def boomareas(cs_points_x, cs_points_z, mesh, t_sk, A_mainspar, A_aftspar, main_spar_loc, aft_spar_loc, debug):

    cs_areasloc_x = (cs_points_x + np.roll(cs_points_x, -1)) / 2
    cs_areasloc_z = (cs_points_z + np.roll(cs_points_z, -1)) / 2
    skin_per, mesh_len = f.get_skin_per(cs_points_x, cs_points_z)
    cs_areas_size = mesh_len * t_sk

    if debug:
        print("Debug mode - spars addition is being skipped")
    else:

        mainspar_max_z = cs_areasloc_z[cs_areasloc_x == main_spar_loc].max()
        mainspar_min_z = cs_areasloc_z[cs_areasloc_x == main_spar_loc].min()
        # b_main = mainspar_max_z - mainspar_min_z
        aftspar_max_z = cs_areasloc_z[cs_areasloc_x == aft_spar_loc].max()
        aftspar_min_z = cs_areasloc_z[cs_areasloc_x == aft_spar_loc].min()
        # b_aft = aftspar_max_z - aftspar_min_z
        cs_areas_size_start = cs_areas_size.copy()
        cs_areas_size[cs_areasloc_x == main_spar_loc] = cs_areas_size[cs_areasloc_x == main_spar_loc] * 2  #thickness is 1mm and not 0.5
        cs_areas_size[cs_areasloc_x == aft_spar_loc] = cs_areas_size[cs_areasloc_x == aft_spar_loc] * 2
        cs_areas_size[np.logical_and(cs_areasloc_x==main_spar_loc, cs_areasloc_z == mainspar_max_z)] = cs_areas_size[np.logical_and(cs_areasloc_x==main_spar_loc, cs_areasloc_z == mainspar_max_z)] + A_mainspar
        cs_areas_size[np.logical_and(cs_areasloc_x == main_spar_loc, cs_areasloc_z == mainspar_min_z)] = cs_areas_size[
                                                                                                             np.logical_and(
                                                                                                                 cs_areasloc_x == main_spar_loc,
                                                                                                                 cs_areasloc_z == mainspar_min_z)] + A_mainspar
        cs_areas_size[np.logical_and(cs_areasloc_x == aft_spar_loc, cs_areasloc_z == aftspar_max_z)] = cs_areas_size[
                                                                                                             np.logical_and(
                                                                                                                 cs_areasloc_x == aft_spar_loc,
                                                                                                                 cs_areasloc_z == aftspar_max_z)] + A_aftspar
        cs_areas_size[np.logical_and(cs_areasloc_x == aft_spar_loc, cs_areasloc_z == aftspar_min_z)] = cs_areas_size[
                                                                                                           np.logical_and(
                                                                                                               cs_areasloc_x == aft_spar_loc,
                                                                                                               cs_areasloc_z == aftspar_min_z)] + A_aftspar


    return cs_areasloc_x, cs_areasloc_z, cs_areas_size, mesh_len, mainspar_min_z, mainspar_max_z, aftspar_min_z, aftspar_max_z


