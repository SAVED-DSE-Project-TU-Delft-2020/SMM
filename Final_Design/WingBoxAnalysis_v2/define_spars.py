import numpy as np

def cut_cs(cs_points_x, mainspar_loc, aft_spar_loc, debug):
    if debug:
        print("Debug mode - cut_cs is being skipped")
    else:
        cs_points_x[cs_points_x < mainspar_loc] = mainspar_loc
        cs_points_x[cs_points_x > aft_spar_loc] = aft_spar_loc

    return cs_points_x