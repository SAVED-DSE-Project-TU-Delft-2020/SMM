'''
author: Marco Desiderio
Concept-A and D structural calculations
Flying wing geometry parameters
'''
class struct_geometry():
    __slots__ = ['b', 'S', 'c_root','c_tip', 'taper', 'sweep', 'c', 'E', 'G', 'sigma_y', 'tau_s', 'MTOM', 'MPAY', 'MBAT', 'OEM']
    def __init__(self):
        #define wing geometry
        self.b = 3
        self.S = 1.3
        self.c_root = 0.76
        self.c_tip = 2*self.S/self.b - self.c_root
        self.taper = self.c_tip/self.c_root
        # print('Taper ratio is: ', self.taper)
        # print('Tip chord is: ', self.c_tip)
        self.sweep = 10 #deg

        self.c = (self.b/2)/(1-self.taper) #height of triangle having root as a base and sides along leading and trailing edges

        #define material properties
        #Alu 7075-T6
        self.E = 71000   # [MPa]
        self.G = 26000   # [MPa]
        self.sigma_y = 505   # [MPa]
        self.tau_s = 331 #[MPa]

        ##wing properties

        self.MTOM = 16.217
        self.MPAY = 3
        self.MBAT = 3.923
        self.OEM = self.MTOM - self.MPAY - self.MBAT

class Parameters(object):
    __slots__ = ['str_par']
    def __init__(self):
        self.str_par = struct_geometry()


def get_parameters(p):
    b = p.str_par.b
    S = p.str_par.S
    c_root = p.str_par.c_root
    c_tip =p.str_par.c_tip
    taper =p.str_par.taper
    sweep =p.str_par.sweep
    c =p.str_par.c  #height of triangle having root as a base and sides along leading and trailing edges
    E =p.str_par.E
    G =p.str_par.G
    sigma_y =p.str_par.sigma_y
    tau_s =p.str_par.tau_s
    MTOM =p.str_par.MTOM
    MPAY =p.str_par.MPAY
    MBAT =p.str_par.MBAT
    OEM =p.str_par.OEM
    return b,S,c_root,c_tip, taper, sweep, c, E, G, sigma_y, tau_s, MTOM, MPAY, MBAT, OEM

