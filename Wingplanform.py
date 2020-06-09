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
    
    # Aft spar location at 65% of the chord
    
    # Wing structural longitudinal CG lies at 70% of distance between main and aft spar at 35 % of the semiwingspan
    
    # Engine longitudinal CG locations at LE intersection
    
    # Engines are placed symmetrically (laterally) at (b/2) 0.35 and (b/2)*0.7

    # x_AC SEAD Torenbeek --> 25 & MAC complete wing lecture 4 BA = 6
    
    # Payload placed on CG location
    
    


#Constraints Input values

wing_loading            = 128.5              #[N/m] from P&P stall
span                    = 3                  #[m]
tipover_angle           = 55                 #[deg]
attachment_root_fin     = 0.15               #[m]

#CG groups

m_engine_inner = 0.3781             #[kg]
m_engine_outer = 0.3781             #[kg]
m_wing_struc   = 8.0                #[kg]
m_avpase       = 0.836              #[kg] Avionics, Parachute and Sensors
m_battery      = 3.6                #[kg] Battery mass
m_payload      = 3                  #[kg] Payload mass
m_fin          = 0.5                #[kg]

x_CG_battery   = 0.10                #[m]
x_CG_avpase    = 0.5                #[m]
gues_x_CG_fin  = 0.65               #[m]


x_CG_without_wing_group = (x_CG_battery * m_battery + x_CG_avpase * m_avpase) / (m_battery+m_avpase)
m_without_wing_group    = m_battery+m_avpase

m_wing_group   = 2* m_engine_inner + 2 * m_engine_outer + m_wing_struc + m_fin

m_total = m_wing_group + m_without_wing_group + m_payload 
print(m_total)
# Subsystem dimensions

width_payload  = 0.268
length_payload = 0.295 
height_payload = 0.118

thickness_pack = 0.042
width_pack = 0.082
length_pack = 0.195
width_battery = length_pack
length_battery = thickness_pack+ width_pack
height_battery = 2*thickness_pack


width_lidar =0.061
length_lidar =0.035
height_lidar  =0.061
# Surface Area

area = m_total *9.80665 / wing_loading

#Bulge Front constraints

flattening = np.sqrt(2)


semi_minor_pl = flattening * height_payload/2
semi_major_pl = np.sqrt((width_payload/2)**2/(1-(height_payload/2)**2/semi_minor_pl**2))

semi_minor_bat = flattening * height_battery/2
semi_major_bat = np.sqrt((width_battery/2)**2/(1-(height_battery/2)**2/semi_minor_bat**2))

semi_minor_lid = flattening * height_lidar/2
semi_major_lid = np.sqrt((width_lidar/2)**2/(1-(height_lidar/2)**2/semi_minor_lid**2))


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
        self.l             = self.calc_l()
        
        
        #target parameters
         
        self.x_NP                 = self.calc_x_NP()
        self.x_CG_wing_struc      = self.calc_x_CG_Wing_struc()
        self.x_CG_engines_outer   = self.calc_x_CG_engines_outer()
        self.x_CG_engines_inner   = self.calc_x_CG_engines_inner()
        self.x_CG_wing_group      = self.calc_x_CG_wing_group()
        self.x_CG                 = self.calc_x_CG()
        self.SM                   = self.calc_SM()
        self.landing_fin_semispan = self.calc_landing_fin_semispan()
        self.c_root_fin           = self.calc_c_root_fin()
        self.sweep_fin_LE         = self.calc_sweep_fin_LE()
        self.x_CG_fin             = self.calc_x_CG_fin()
        
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
        x_CG_wing_struc =  np.tan(self.sweep_LE) * (0.35 * self.span / 2) + (0.10 + 0.55 * 0.7) * c_35
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
        x_CG_wing_group = (gues_x_CG_fin*m_fin + self.x_CG_wing_struc * m_wing_struc + 2*(self.x_CG_engines_outer*m_engine_outer) + 2*(self.x_CG_engines_inner*m_engine_inner)) / (m_wing_group)
        return x_CG_wing_group
        
    def calc_x_CG(self):
        x_CG = (x_CG_without_wing_group * m_without_wing_group + self.x_CG_wing_group * m_wing_group) / (m_without_wing_group + m_wing_group + m_payload) 
        return x_CG
    
    def calc_SM(self):
        SM = ( self.x_NP - self.x_CG ) / self.c_MAC
        return SM
    
    def calc_l(self):
        l = (np.tan(self.sweep_LE) * self.span/2 + self.c_tip)
        return l
    
    def calc_landing_fin_semispan(self):
        phi = tipover_angle/180*np.pi
        b = (self.l-self.x_CG) / np.tan(phi)
        beta = np.arcsin(b/(self.span/2))
        alpha = np.pi/2 - beta
        landing_fin_semispan = b / np.sin(alpha)
        return landing_fin_semispan
    
    def calc_c_root_fin(self):
        c_root_fin = self.l - self.c_root + attachment_root_fin
        return c_root_fin
    
    def calc_sweep_fin_LE(self):
        sweep_LE_fin = np.arctan(self.c_root_fin/ self.landing_fin_semispan)
        return sweep_LE_fin

    def calc_x_CG_fin(self):
        a = 0.35 # input for centroid as function of total longitudinal length
        x_CG_fin = self.c_root - attachment_root_fin + self.c_root_fin * a
        return x_CG_fin
    
    
    
    
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
        if Data.SM > 0.100 and Data.SM < 0.101:
            ax.plot(m,n,'ro', markersize=1)
            options.append([round(n,3),round(m,3)])
            #print("For taper = " + str(round(m,3)) + " and for sweep = " +str(round(n,3)) + " degrees, SM = " + str(Data.SM))
        if Data.SM > 0.175 and Data.SM < 0.176:
            ax.plot(m,n,'bo', markersize=1)
            #print("For taper = " + str(round(m,3)) + " and for sweep = " +str(round(n,3)) + " degrees, SM = " + str(Data.SM))
        if Data.SM > 0.200 and Data.SM < 0.201:
            ax.plot(m,n,'ko', markersize=1)
            #print("For taper = " + str(round(m,3)) + " and for sweep = " +str(round(n,3)) + " degrees, SM = " + str(Data.SM))

#print(options)
MinSweep = [min(idx) for idx in zip(*options)][0]

''' Draw Geometry (topview) '''

# Inputs

g = 0.35
s = 20
Data = Planform(area,span,g,s)

print("Root chorr:", Data.c_root)
print("Tip chord:", Data.c_tip)

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

#bulge constraint
point_pl2 = (-semi_major_pl, Data.x_CG - length_payload/2)
point_pr2 = (semi_major_pl,Data.x_CG - length_payload/2)
point_pr1 = (semi_major_pl,Data.x_CG + length_payload/2)
point_pl1 = (-semi_major_pl,Data.x_CG + length_payload/2)


#Battery
point_18 = (-width_battery/2, Data.x_CG - length_payload/2-0.005)
point_19 = (-width_battery/2, Data.x_CG - length_payload/2 - length_battery -0.005)
point_20 = (width_battery/2,Data.x_CG - length_payload/2 - length_battery-0.005)
point_21 = (width_battery/2,Data.x_CG - length_payload/2-0.005)

#Lidar

point_38 = (-width_lidar/2, Data.x_CG - length_payload/2-length_battery-0.01)
point_39 = (-width_lidar/2, Data.x_CG - length_payload/2 - length_battery - length_lidar-0.01)
point_40 = (width_lidar/2,Data.x_CG - length_payload/2 - length_battery-length_lidar-0.01)
point_41 = (width_lidar/2, Data.x_CG - length_payload/2-length_battery-0.01)

#nosecone
a_nose_top  = semi_major_pl
b_nose_top = np.sqrt((Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01-(Data.x_CG - length_payload/2))**2/(1-(semi_minor_lid)**2/semi_minor_pl**2))


x = np.linspace(-semi_major_pl,semi_major_pl,100)
y = -np.sqrt((1-x**2/a_nose_top**2)*b_nose_top**2)+(Data.x_CG - length_payload/2)

#tailcone
point_tail = (0,Data.c_root)
point_left = (-semi_major_pl,Data.x_CG + length_payload/2)
point_right = (semi_major_pl,Data.x_CG + length_payload/2)







# Plot points

wingplanform        = plt.figure()
ax                  = wingplanform.add_subplot()
points_outline      = [point_1, point_2, point_3, point_4, point_5, point_6]
points_quarterchord = [point_7,point_8,point_9]
points_MAC_r        = [point_10,point_11]
points_MAC_l        = [point_12,point_13]
points_payload      = [point_14,point_15,point_17,point_16]
points_bulge_pr = [point_pr1,point_pr2]
points_bulge_pl = [point_pl1,point_pl2]
points_battery      = [point_18,point_19,point_20,point_21]
points_lidar        = [point_38,point_39,point_40,point_41]
points_tail_left    = [point_tail,point_left]
points_tail_right   = [point_tail,point_right]

line_outline        = plt.Polygon(points_outline, closed=True, fill=None, edgecolor='r')
line_quarterchord   = plt.Polygon(points_quarterchord, closed=None, fill=None, edgecolor='r')
line_MAC_r          = plt.Polygon(points_MAC_r, closed=None, fill=None, edgecolor='b')
line_MAC_l          = plt.Polygon(points_MAC_l, closed=None, fill=None, edgecolor='b')
line_payload        = plt.Polygon(points_payload, closed=True, fill=None, edgecolor='r')
line_bulge_pr = plt.Polygon(points_bulge_pr, closed=True, fill=None, edgecolor='r')
line_bulge_pl = plt.Polygon(points_bulge_pl, closed=True, fill=None, edgecolor='r')
line_battery        = plt.Polygon(points_battery, closed=True, fill=None, edgecolor='y')
line_lidar          = plt.Polygon(points_lidar, closed=True, fill=None, edgecolor='g')
line_tail_left      = plt.Polygon(points_tail_left, closed=True, fill=None, edgecolor='b')
line_tail_right     =plt.Polygon(points_tail_right, closed=True, fill=None, edgecolor='b')

wingplanform.gca().add_line(line_MAC_r)
wingplanform.gca().add_line(line_MAC_l)
wingplanform.gca().add_line(line_outline)
wingplanform.gca().add_line(line_quarterchord)
wingplanform.gca().add_line(line_payload)
wingplanform.gca().add_line(line_battery)
wingplanform.gca().add_line(line_lidar)
wingplanform.gca().add_line(line_bulge_pr)
wingplanform.gca().add_line(line_bulge_pl)
wingplanform.gca().add_line(line_tail_left)
wingplanform.gca().add_line(line_tail_right)

ax.plot(0,Data.x_CG, 'ro')
ax.plot(0,Data.x_NP, 'bo')
ax.plot(0,Data.x_CG_wing_struc, 'go')
ax.plot(0,x_CG_battery, 'yo')
ax.plot(0.35*Data.span/2,Data.x_CG_engines_inner, 'rx')
ax.plot(0.70*Data.span/2,Data.x_CG_engines_outer, 'rx')
ax.plot(-0.35*Data.span/2,Data.x_CG_engines_inner, 'rx')
ax.plot(-0.7*Data.span/2,Data.x_CG_engines_outer, 'rx')
ax.plot(x,y)
ax.axis('equal')
ax.grid(True)


"""Draw side view"""


sideview = plt.figure()
ax = sideview.add_subplot()

#Payload

point_22 = (Data.x_CG - length_payload/2, -height_payload/2)
point_23 = (Data.x_CG - length_payload/2,+height_payload/2)
point_24 = (Data.x_CG + length_payload/2,+height_payload/2)
point_25 = (Data.x_CG + length_payload/2,-height_payload/2)


#bulge constraint
point_pb2 = (Data.x_CG - length_payload/2, -semi_minor_pl)
point_pt2 = (Data.x_CG - length_payload/2,semi_minor_pl)
point_pt1 = (Data.x_CG + length_payload/2,semi_minor_pl)
point_pb1 = (Data.x_CG + length_payload/2,-semi_minor_pl)



#Battery

point_26 = (Data.x_CG - length_payload/2-0.005,-thickness_pack)
point_27 = (Data.x_CG - length_payload/2-0.005,thickness_pack)
point_28 = (Data.x_CG - length_payload/2-width_pack-0.005,thickness_pack)
point_29 = (Data.x_CG - length_payload/2-width_pack-0.005,width_pack/2)
point_30 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.005,width_pack/2)
point_31 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.005,-width_pack/2)
point_32 = (Data.x_CG - length_payload/2-width_pack-0.005,-width_pack/2)
point_33 = (Data.x_CG - length_payload/2-width_pack-0.005,-thickness_pack)

print("Input Fin c.g.:", gues_x_CG_fin)
print("Actual Fin c.g.:", Data.x_CG_fin)
print("Input battery c.g.:", x_CG_battery)
print("Actual battery c.g.:", Data.x_CG - length_payload/2-width_pack/2-thickness_pack/2-0.005 )

print("Payload c.g.: ", Data.x_CG)

print("outer engine: ", Data.x_CG_engines_outer)
print("inner engine: ", Data.x_CG_engines_inner)


#Lidar

point_34 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.01,height_lidar/2)
point_35 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01,height_lidar/2)
point_36 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01,-height_lidar/2)
point_37 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.01,-height_lidar/2)

#bulge constraint
point_lt1 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.01, +semi_minor_lid)
point_lb2 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01,-semi_minor_lid)
point_lt2 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01,semi_minor_lid)
point_lb1 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.01,-semi_minor_lid)



#nosecone

b_nose_side = semi_minor_pl
a_nose_side  = b_nose_top

x = np.linspace(point_pt2[0]-a_nose_side,point_pt2[0],100)
s_y_top = np.sqrt(b_nose_side**2*(1-(x-point_pt2[0])**2/a_nose_side**2))
s_y_bottom = -np.sqrt(b_nose_side**2*(1-(x-point_pt2[0])**2/a_nose_side**2))

#tailcone
point_tail = (Data.c_root,0)
point_top = (Data.x_CG + length_payload/2,semi_minor_pl)
point_bottom = (Data.x_CG + length_payload/2,-semi_minor_pl)




s_points_payload = [point_22,point_23, point_24, point_25]
s_points_bulge_pt = [point_pt1,point_pt2]
s_points_bulge_pl = [point_pb1,point_pb2]
s_points_battery = [point_26,point_27, point_28, point_29,point_30,point_31,point_32,point_33]
s_points_lidar = [point_34,point_35,point_36,point_37]
s_points_bulge_lt = [point_lt1,point_lt2]
s_points_bulge_lb = [point_lb1,point_lb2]
s_points_tail_top = [point_top,point_tail]
s_points_tail_bottom = [point_bottom,point_tail]

s_line_payload = plt.Polygon(s_points_payload,closed=True, fill=None, edgecolor='r')
s_line_bulge_pt = plt.Polygon(s_points_bulge_pt,closed=True, fill=None, edgecolor='r')
s_line_bulge_pl = plt.Polygon(s_points_bulge_pl,closed=True, fill=None, edgecolor='r')
s_line_battery = plt.Polygon(s_points_battery,closed=True, fill=None, edgecolor='y')
s_line_lidar = plt.Polygon(s_points_lidar,closed=True, fill=None, edgecolor='g')
s_line_bulge_lt = plt.Polygon(s_points_bulge_lt,closed=True, fill=None, edgecolor='g')
s_line_bulge_ll = plt.Polygon(s_points_bulge_lb,closed=True, fill=None, edgecolor='g')
s_line_tail_top = plt.Polygon(s_points_tail_top,closed=True, fill=None, edgecolor='b')
s_line_tail_bottom = plt.Polygon(s_points_tail_bottom,closed=True, fill=None, edgecolor='b')


sideview.gca().add_line(s_line_payload)
sideview.gca().add_line(s_line_bulge_pt)
sideview.gca().add_line(s_line_bulge_pl)
sideview.gca().add_line(s_line_battery)
sideview.gca().add_line(s_line_lidar)
#sideview.gca().add_line(s_line_bulge_lt)
#sideview.gca().add_line(s_line_bulge_ll)
sideview.gca().add_line(s_line_tail_bottom)
sideview.gca().add_line(s_line_tail_top)
ax.plot(x,s_y_top)
ax.plot(x,s_y_bottom)
ax.axis('equal')
ax.grid(True)


"""Frontview"""
frontview = plt.figure()
ax = frontview.add_subplot()

#Payload

point_38 = (- width_payload/2, -height_payload/2)
point_39 = ( - width_payload/2,+height_payload/2)
point_40 = (width_payload/2,+height_payload/2)
point_41 = (width_payload/2,-height_payload/2)

#bulge

x = np.linspace(-semi_major_pl,semi_major_pl,100)
y_top = np.sqrt(semi_minor_pl**2*(1-x**2/semi_major_pl**2))
y_bottom = -np.sqrt(semi_minor_pl**2*(1-x**2/semi_major_pl**2))

#Lidar
#
# point_34 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.01,height_lidar/2)
# point_35 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01,height_lidar/2)
# point_36 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-length_lidar-0.01,-height_lidar/2)
# point_37 = (Data.x_CG - length_payload/2-width_pack-thickness_pack-0.01,-height_lidar/2)


f_points_payload = [point_38,point_39, point_40, point_41]

f_line_payload = plt.Polygon(f_points_payload,closed=True, fill=None, edgecolor='r')



frontview.gca().add_line(f_line_payload)

ax.axis('equal')
ax.plot(x,y_top)
ax.plot(x,y_bottom)
ax.grid(True)

plt.show()



""""CONTROL POINT DEFINITION"""


N = 100

xs = np.linspace(Data.x_CG - length_payload/2-a_nose_side,Data.c_root,N)

control_points = []
for x in xs:
    if x<(Data.x_CG - length_payload/2):
        h1 = Data.x_CG - length_payload/2
        y_left = -np.sqrt((1-(x-h1)**2/b_nose_top**2)*a_nose_top**2)
        y_right= +np.sqrt((1-(x-h1)**2/b_nose_top**2)*a_nose_top**2)
        z_top = np.sqrt(b_nose_side**2*(1-(x-h1)**2/a_nose_side**2))
        z_bottom = -np.sqrt(b_nose_side**2*(1-(x-h1)**2/a_nose_side**2))
    elif (Data.x_CG - length_payload/2)  <=  x  <  (Data.x_CG + length_payload/2):
        y_left = -a_nose_top
        y_right = a_nose_top
        z_top  = b_nose_side
        z_bottom = -b_nose_side
    else:
        h2 = Data.x_CG + length_payload/2
        y_left  = -a_nose_top+(x-h2)*a_nose_top/(Data.c_root-h2)
        y_right =a_nose_top-(x-h2)*a_nose_top/(Data.c_root-h2)
        z_top   =  b_nose_side - (x-h2)*b_nose_side/(Data.c_root-h2)
        z_bottom =  -b_nose_side +(x-h2)*b_nose_side/(Data.c_root-h2)
    control_points.append([x,y_left,y_right,z_top,z_bottom])
    
def generate_ellipses(points,filename):
    """"
    points = 2D array of sideview control points [[x,yleft,yright,ztop,zbottom]]
    filename = Name of the file to write the coordinates to 
    """ 
    file = open(filename,"w")
    file.close()
    
    file = open(str(filename)+".txt","w")
    lines_start = ["BODYTYPE","\n","1","\nOFFSET","\n","0","\t","0","\t","0"]
    file.writelines(lines_start)

    n = len(points)
    
    ellipse_data = [] 
    
    for i in range(n):
        if i == 0 or i == n - 1:
            theta = np.linspace(0,2*np.pi,70)
            
            y_data = []
            z_data = []
            index_data = []
            for k in range(len(theta)): 
                y_data.append(0)
                z_data.append(0)
                index_data.append(points[i][0])
            ellipse_data.append([index_data,y_data,z_data])
            
            lines_frame = ["\nFRAME"]
            file.writelines(lines_frame)
            for i in range(len(index_data)):
                line = ["\n",str(index_data[i]),"\t",str(y_data[i]),"\t",str(z_data[i])]
                file.writelines(line)
            lines_end = ["\n"]
            file.writelines(lines_end)
        
        else:
            a = np.abs(points[i][1] - points[i][2])/2
            b = np.abs(points[i][3] - points[i][4])/2
        
            theta = np.linspace(0,2*np.pi,70)
            r = a*b/np.sqrt(a**2*np.sin(theta)**2+b**2*np.cos(theta)**2)


            y_data = r*np.cos(theta)
            z_data = r*np.sin(theta)

            index_data = np.zeros(len(y_data))
            for k in range(len(index_data)):
                index_data[k] = points[i][0]
            ellipse_data.append([index_data,y_data,z_data])
        
            lines_frame = ["\nFRAME"]
            file.writelines(lines_frame)
            for i in range(len(index_data)):
                line = ["\n",str(index_data[i]),"\t",str(y_data[i]),"\t",str(z_data[i])]
                file.writelines(line)
            lines_end = ["\n"]
            file.writelines(lines_end)

    file.close()
    
    return ellipse_data

ellipse_data = generate_ellipses(control_points,"body")

plt.plot(ellipse_data[10][1],ellipse_data[10][2])

### Semi-empirical twist estimation method
        
CL_design = 0.4 #0.28-0.35

beta_required  = 19 *(CL_design/1)*(0.06/0.1)
beta_cm        = 11 *(0.018/0.05)
alpha_morphing = 0 #no airfoil morphing (aerodynamic twist)

beta = beta_required - beta_cm - alpha_morphing        







