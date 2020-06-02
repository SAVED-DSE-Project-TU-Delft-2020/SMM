#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:38:34 2020

@author: Axel
"""
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd

''' MODEL ASSUMPTIONS '''

    # Aircraft symmetrical along longitudinal (x) - axis

    # Forward spar location at 10% of the Chord
    
    # Aft spar location at 60% of the chord
    
    # Wing structural longitudinal CG lies at 70% of distance between main and aft spar at 35 % of the semiwingspan
    
    # Engine longitudinal CG locations at LE intersection
    
    # Engines are placed symmetrically (laterally) at (b/2) 0.35 and (b/2)*0.7

    # x_AC SEAD Torenbeek --> 25 & MAC complete wing lecture 4 BA = 6
    
    # Payload placed on CG location
    
    


#Constraints Input values

wing_loading   = 122                #[N/m] from P&P stall
span           = 3                  #[m]

#CG groups

m_engine_inner = 0.4                #[kg]
m_engine_outer = 0.4                #[kg]
m_wing_struc   = 8.5                #[kg]
m_avpase       = 0.836 - 0.5        #[kg] Avionics, Parachute and Sensors
m_battery      = 3.6                #[kg] Battery mass
m_payload      = 3                  #[kg] Payload mass

x_CG_battery   = 0.15               #[m]
x_CG_avpase    = 0.35               #[m]

x_CG_without_wing_group = (x_CG_battery * m_battery + x_CG_avpase * m_avpase) / (m_battery+m_avpase)
m_without_wing_group    = m_battery+m_avpase

m_wing_group   = 2* m_engine_inner + 2 * m_engine_outer + m_wing_struc

m_total = m_wing_group + m_without_wing_group + m_payload

# Subsystem dimensions

width_payload  = 0.268
length_payload = 0.295 
height_payload = 0.118

# Surface Area

area = m_total *9.80665 / wing_loading


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
        c_35 = 2 * self.area / ((1+self.taper) * self.span) * (1 - (1 - self.taper) / self.span * (2 * 0.35 * self.span / 2))
        x_CG_wing_struc =  np.tan(self.sweep_LE) * (0.35 * self.span / 2) + (0.10 + 0.5 * 0.7) * c_35
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
        x_CG = (x_CG_without_wing_group * m_without_wing_group + self.x_CG_wing_group * m_wing_group) / (m_without_wing_group + m_wing_group + m_payload) 
        return x_CG
    
    def calc_SM(self):
        SM = ( self.x_NP - self.x_CG ) / self.c_MAC
        return SM
    
    
taperlist = np.arange(0.1,1,0.01)
sweeplist = np.arange(0,25,0.1)   



graphSM = plt.figure()
ax = graphSM.add_subplot()

#ax.xlabel('Taper Ratio [C_t/C_r]')
#ax.ylabel('Sweep q(1/4) [deg]')
ax.grid(True)
ax.set_title('Sweep vs Taper for SM = 20 (red), 17.5 (blue), and 15 (black)')

options = []

for m in taperlist:
    for n in sweeplist:
        Data = Planform(area,span,m,n)
        if Data.SM > 0.200 and Data.SM < 0.201:
            ax.plot(m,n,'ro', markersize=1)
            options.append([round(n,3),round(m,3)])
            #print("For taper = " + str(round(m,3)) + " and for sweep = " +str(round(n,3)) + " degrees, SM = " + str(Data.SM))
        if Data.SM > 0.175 and Data.SM < 0.176:
            ax.plot(m,n,'bo', markersize=1)
            #print("For taper = " + str(round(m,3)) + " and for sweep = " +str(round(n,3)) + " degrees, SM = " + str(Data.SM))
        if Data.SM > 0.150 and Data.SM < 0.151:
            ax.plot(m,n,'ko', markersize=1)
            #print("For taper = " + str(round(m,3)) + " and for sweep = " +str(round(n,3)) + " degrees, SM = " + str(Data.SM))

#print(options)
MinSweep = [min(idx) for idx in zip(*options)][0]

''' Draw Geometry '''

# Inputs

g = 0.4
s = MinSweep
Data = Planform(area,span,g,s)

# Define points

# Planform
point_1 = (-Data.span/2, np.tan(Data.sweep_LE)* Data.span/2 + Data.c_tip)
point_2 = (-Data.span/2, np.tan(Data.sweep_LE)* Data.span/2)
point_3 = (0,0)
point_4 = (Data.span/2,np.tan(Data.sweep_LE)* Data.span/2 )
point_5 = (Data.span/2,np.tan(Data.sweep_LE)* Data.span/2 + Data.c_tip)
point_6 = (0,Data.c_root)

#25%chordline
point_7 = (-Data.span/2,np.tan(Data.sweep)* Data.span/2 + Data.c_root * 0.25)
point_8 = (0,Data.c_root * 0.25)
point_9 = (Data.span/2,np.tan(Data.sweep)* Data.span/2 + Data.c_root * 0.25)

#MAC
point_10 = (Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC)
point_11 = (Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC + Data.c_MAC) 

point_12 = (-Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC)
point_13 = (-Data.y_MAC,np.tan(Data.sweep_LE)*Data.y_MAC + Data.c_MAC) 

#Payload
point_14 = (-width_payload/2, Data.x_CG + length_payload/2)
point_15 = (width_payload/2, Data.x_CG + length_payload/2)
point_16 = (-width_payload/2, Data.x_CG - length_payload/2)
point_17 = (width_payload/2, Data.x_CG - length_payload/2)

# Plot points

wingplanform        = plt.figure()
ax                  = wingplanform.add_subplot()
points_outline      = [point_1, point_2, point_3, point_4, point_5, point_6]
points_quarterchord = [point_7,point_8,point_9]
points_MAC_r        = [point_10,point_11]
points_MAC_l        = [point_12,point_13]
points_payload      = [point_14,point_15,point_17,point_16]

line_outline        = plt.Polygon(points_outline, closed=True, fill=None, edgecolor='r')
line_quarterchord   = plt.Polygon(points_quarterchord, closed=None, fill=None, edgecolor='r')
line_MAC_r          = plt.Polygon(points_MAC_r, closed=None, fill=None, edgecolor='b')
line_MAC_l          = plt.Polygon(points_MAC_l, closed=None, fill=None, edgecolor='b')
line_payload        = plt.Polygon(points_payload, closed=True, fill=None, edgecolor='r')

wingplanform.gca().add_line(line_MAC_r)
wingplanform.gca().add_line(line_MAC_l)
wingplanform.gca().add_line(line_outline)
wingplanform.gca().add_line(line_quarterchord)
wingplanform.gca().add_line(line_payload)

ax.plot(0,Data.x_CG, 'ro')
ax.plot(0,Data.x_NP, 'bo')
ax.plot(0,Data.x_CG_wing_struc, 'go')
ax.plot(0.35*Data.span/2,Data.x_CG_engines_inner, 'rx')
ax.plot(0.70*Data.span/2,Data.x_CG_engines_outer, 'rx')
ax.plot(-0.35*Data.span/2,Data.x_CG_engines_inner, 'rx')
ax.plot(-0.7*Data.span/2,Data.x_CG_engines_outer, 'rx')
ax.axis('equal')
ax.grid(True)

plt.show()















