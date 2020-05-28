#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:38:34 2020

@author: Axel
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

''' MODEL ASSUMPTIONS '''

    # Forward spar location at 25% of the Chord
    
    # Aft spar location at 75% of the chord
    
    # Engine longitudinal CG locations at LE intersection
    
    # Engines are placed symmetrically (laterally) at (b/2) 0.35 and (b/2)*0.7

    # 


#Input values

m_engine_inner = 1                  #[kg]
m_engine_outer = 1                  #[kg]
m_wing_struc   = 8.7                #[kg]
area           = 1.3                #[m^2]
span           = 3                  #[m]
sweep          = 0 * np.pi / 180    #[rad]
x_CG_without_wing_group  = 0.15     #[m]
m_without_wing_group     = 7.46

m_wing_group   = 2* m_engine_inner + 2 * m_engine_outer + m_wing_struc

class Planform:
    
    def __init__(self,area,span,taper,sweep):
        
        #input parameter definitions
        
        self.area     = area                    # [m]
        self.span     = span                    # [m] 
        self.taper    = taper                   # []
        self.sweep    = sweep * np.pi /180      # [rad] quarter chord     
       
        #intermediary planform definitions
        
        self.c_root        = self.calc_c_root()
        self.c_tip         = self.calc_c_tip()
        self.c_MAC         = self.calc_c_MAC()
        self.y_MAC         = self.calc_y_MAC()
        self.sweep_LE      = self.calc_sweep_LE()
        
        #target parameters
        
        self.x_NP               = self.calc_x_NP()
        self.x_CG_wing_struc    = self.calc_x_CG_Wing_struc()
        self.x_CG_engines_outer = self.calc_x_CG_engines_outer()
        self.x_CG_engines_inner = self.calc_x_CG_engines_inner()
        self.x_CG_wing_group    = self.calc_x_CG_wing_group()
        self.x_CG               = self.calc_x_CG()
        self.SM                 = self.calc_SM()
        
    def calc_c_root(self):
        c_root = self.area * 2 / self.span / ( 1 + self.taper )  
        return c_root
    
    def calc_c_tip(self):
        c_tip = self.c_root * self.taper
        return c_tip
    
    def calc_c_MAC(self):
        c_MAC = 2 / 3 * ( 1 + self.taper + self.taper ** 2) / ( 1 + self.taper )  * (self.c_root)
        return c_MAC

    def calc_y_MAC(self):
        y_MAC = self.span / 2 * (self.c_root - self.c_MAC) / (self.c_root - self.c_tip)
        return y_MAC
    
    def calc_sweep_LE(self):
        sweep_LE = np.arctan(( self.span / 2 * np.tan(self.sweep) + 0.25 * self.c_root * ( 1 - self.taper))/( self.span / 2))
        return sweep_LE
    
    def calc_x_NP(self): # source: https://www.mh-aerotools.de/airfoils/flywing1.htm
        if self.taper > 0.375:
           x_NP = ( 0.25 * self.c_root) + ( 2 * self.span ) / ( 3 * np.pi) * np.tan(self.sweep)
        if self.taper < 0.375:
           x_NP =  0.25 * self.c_root + ( self.span * ( 1 + 2 * self.taper )) / (6 * ( 1 + self.taper )) * np.tan(self.sweep)
        return x_NP
    
    def calc_x_CG_Wing_struc(self):
        x_CG_wing_struc = 0.25 * self.c_root + np.tan(self.sweep) * (0.35 * self.span / 2)
        return x_CG_wing_struc
    
    def calc_x_CG_engines_outer(self):
        a = 0 # def extra c.g. in case engines stick out of the wing
        x_CG_engines_outer = np.tan(self.sweep_LE) * 0.7 * ( self.span / 2) + a
        return x_CG_engines_outer

    def calc_x_CG_engines_inner(self):
        a = 0 # def extra c.g. in case engines stick out of the wing
        x_CG_engines_inner = np.tan(self.sweep_LE) * 0.35 * ( self.span / 2) + a
        return x_CG_engines_inner
    
    def calc_x_CG_wing_group(self):
        x_CG_wing_group = (self.x_CG_wing_struc * m_wing_struc + 2*(self.x_CG_engines_outer*m_engine_outer) + 2*(self.x_CG_engines_inner*m_engine_inner)) / (m_wing_struc+2*m_engine_outer+2*m_engine_inner)
        return x_CG_wing_group
        
    def calc_x_CG(self):
        x_CG = (x_CG_without_wing_group * m_without_wing_group + self.x_CG_wing_group * m_wing_group) / (m_without_wing_group + m_wing_group)
        return x_CG
    
    def calc_SM(self):
        SM = ( self.x_NP - self.x_CG ) 
        return SM
    
    
taperlist = np.arange(0.1,1,0.05)
sweeplist = np.arange(0,40,5)   
        

for j in taperlist:
    
    Data_0 = Planform(area,span,j,0)
    Data_5 = Planform(area,span,j,5)
    Data_10 = Planform(area,span,j,10)
    Data_15 = Planform(area,span,j,15)
    Data_20 = Planform(area,span,j,20)
    Data_25 = Planform(area,span,j,25)


#    plt.plot(j,Data_0.x_NP,'bx')
#    plt.plot(j,Data_0.x_CG,'ro')
#    plt.plot(j,Data_0.SM,'ko')


    
''' Draw Geometry '''

# Inputs

g = 0.5
s = 2
Data = Planform(area,span,g,s)

# Define points

point_1 = (-Data.span/2, np.tan(Data.sweep_LE)* Data.span/2 + Data.c_tip)
point_2 = (-Data.span/2, np.tan(Data.sweep_LE)* Data.span/2)
point_3 = (0,0)
point_4 = (Data.span/2,np.tan(Data.sweep_LE)* Data.span/2 )
point_5 = (Data.span/2,np.tan(Data.sweep_LE)* Data.span/2 + Data.c_tip)
point_6 = (0,Data.c_root)

point_7 = (-Data.span/2,np.tan(Data.sweep)* Data.span/2 + Data.c_root * 0.25)
point_8 = (0,Data.c_root * 0.25)
point_9 = (Data.span/2,np.tan(Data.sweep)* Data.span/2 + Data.c_root * 0.25)

point_10 = (Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC)
point_11 = (Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC + Data.c_MAC) 

point_12 = (-Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC)
point_13 = (-Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC + Data.c_MAC) 


# Plot points
points_outline = [point_1, point_2, point_3, point_4, point_5, point_6]
points_quarterchord = [point_7,point_8,point_9]
points_MAC_r = [point_10,point_11]
points_MAC_l = [point_12,point_13]

line_outline = plt.Polygon(points_outline, closed=True, fill=None, edgecolor='r')
line_quarterchord = plt.Polygon(points_quarterchord, closed=None, fill=None, edgecolor='r')
line_MAC_r = plt.Polygon(points_MAC_r, closed=None, fill=None, edgecolor='r')
line_MAC_l = plt.Polygon(points_MAC_l, closed=None, fill=None, edgecolor='r')

plt.gca().add_line(line_MAC_r)
plt.gca().add_line(line_MAC_l)
plt.gca().add_line(line_outline)
plt.gca().add_line(line_quarterchord)

plt.plot(0,Data.x_CG, 'ro')
plt.plot(0,Data.x_NP, 'bo')
plt.plot(0,Data.x_CG, 'rx')
plt.plot(0,Data.x_NP, 'rx')
plt.plot(0,Data.x_CG, 'rx')
plt.plot(0,Data.x_NP, 'rx')
plt.axis('equal')
plt.grid(True)
plt.show()













