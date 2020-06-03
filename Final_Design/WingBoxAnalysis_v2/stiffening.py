import numpy as np
import functions as f

def stiffen_CS(cs_areasloc_x, cs_areasloc_z, cs_areasize, stiff_linecoord, stiffeners_size):
    for stiffener in stiff_linecoord:
        area_temp = stiffeners_size[stiff_linecoord == stiffener]
        print(area_temp)
        x_temp = cs_areasloc_x[stiffener]
        z_temp = cs_areasloc_z[stiffener]
        print(cs_areasize[stiffener])
        cs_areasize[stiffener] = cs_areasize[stiffener] + area_temp
        print(cs_areasize[stiffener])
    return cs_areasize