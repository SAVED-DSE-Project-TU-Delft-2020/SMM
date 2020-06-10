import numpy as np



def compute_axial_buckling(k, E, v, t, b):
    sigma_cr = (k * np.pi**2 * E / (12 * (1 - v**2))) * (t / b)**2
    return  sigma_cr
def compute_shear_buckling(k, E, v, t, b):
    tau_cr = (k * np.pi ** 2 * E / (12 * (1 - v ** 2))) * (t / b) ** 2
    return tau_cr