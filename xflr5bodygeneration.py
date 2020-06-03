# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:45:40 2020

@author: Casper

This function transforms a sideview to a selection of ellipses in order to import the body into XFLR5. 
"""
# =============================================================================
# Importing relevant modules 
import numpy as np 
from matplotlib import pyplot as plt

# =============================================================================
# Functions
def generate_ellipses(points,filename):
    """"
    points = 2D array of sideview control points [[x,yleft,yright,ztop,zbottom]]
    filename = Name of the file to write the coordinates to 
    """ 
    file = open(filename,"w")
    file.close()
    
    file = open(str(filename)+".txt","w")
    lines_start = ["BODYTYPE","\n","2","\nOFFSET","\n","0","\t","0","\t","0"]
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
            a = np.abs(points[i][1] - points[i][2])
            b = np.abs(points[i][3] - points[i][4])
            e = np.sqrt(1 - (b**2/a**2))
        
            theta = np.linspace(0,2*np.pi,70)
            r = (a*(1-e**2))/(1-e*np.cos(theta))
       
            y_data = []
            z_data = []
            for j in range(len(theta)): 
                y = r[j]*np.cos(theta[j])
                z = r[j]*np.sin(theta[j])
                y_data.append(y)
                z_data.append(z)
            
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
        
        
# =============================================================================
# Test
points_test = [[0,1,-1,1,-1],[1,1,-1,1,-1],[2,1,-1,1,-1],[3,1,-1,1,-1],[4,1,-1,1,-1],[5,1,-1,1,-1],[6,1,-1,1,-1],[7,1,-1,1,-1]]
ellipse_data = generate_ellipses(points_test,"body")

plt.plot(ellipse_data[0][1],ellipse_data[0][2])

