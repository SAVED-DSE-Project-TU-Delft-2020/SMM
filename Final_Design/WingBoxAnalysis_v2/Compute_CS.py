import numpy as np
import matplotlib.pyplot as plt
import parameters as par
import functions as f

def compute_centroid(cs_areapoints_x, cs_areapoints_z, cs_boomareas):
    x_bar = np.sum(cs_boomareas * cs_areapoints_x) / np.sum(cs_boomareas)
    z_bar = np.sum(cs_boomareas * cs_areapoints_z) / np.sum(cs_boomareas)
    return x_bar, z_bar
def compute_SMOA(cs_areapoints_x, cs_areapoints_z, cs_boomareas, x_bar, z_bar):
    Ixx = np.sum(cs_boomareas * (cs_areapoints_z - z_bar)**2)
    Izz = np.sum(cs_boomareas * (cs_areapoints_x - x_bar)**2)
    Izx = np.sum(cs_boomareas * (cs_areapoints_x - x_bar) * (cs_areapoints_z - z_bar))
    return Ixx, Izz, Izx