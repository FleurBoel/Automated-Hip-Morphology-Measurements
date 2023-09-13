# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 13:22:23 2021

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np

def perp_dist(p0, p1, p2):
    """
    This function calculates the perpendicular distance between a point (p0) 
    and a line defined by the points p1 and p2.
    
    Parameters
    ----------
    p0 : array of float
        The x- and y-coordinates of p0, 1D array.
    p1 : array of float
        The x- and y-coordinates of p1, 1D array.
    p2 : array of float
        The x- and y-coordinates of p2, 1D array.

    Returns
    -------
    dist : float
        Perpendicular distance between the point p0 and the line defined by 
        points p1 and p2.
        
    dist = |A*x_p + B*y_p + C| / sqrt(A^2 + B^2)
    
    where A = slope = dy/dx, B = -1, C = intercept = y-slope*x

    """
    A = (p2[1]-p1[1])/(p2[0]-p1[0])
    B = -1
    C = p2[1] - A*p2[0]
     
    dist = abs(A*p0[0] + B*p0[1] + C) / np.sqrt(A**2 + B**2)
    
    return dist

def dist_2_points(p0, p1):
    """
    This function calculates the Euclidean distance between the points p0 and p1.

    Parameters
    ----------
    p0 : array of float
        The x- and y-coordinates of p0, 1D array.
    p1 : array of float
        The x- and y-coordinates of p1, 1D array.

    Returns
    -------
    dist : float
        Distance between points p0 and p1.
    
    dist = sqrt(dx^2 + dy^2)

    """
    
    dist = np.sqrt((p1[0]- p0[0])**2 + (p1[1] - p0[1])**2)
    
    return dist

def perp_dist_line(p, slope, intercept):   
    """
    This function calculates the perpendicular distance between a point (p) and 
    a line defined by the slope and intercept
    
    Parameters
    ----------
    p  : array of float
        The x- and y-coordinates of point p, 1D array.
    slope : float
        Slope of the line.
    intercept : float
        Intercept of the line.

    Returns
    -------
    dist : float
        Perpendicular distance between the point p and the line defined by 
        the slope and intercept.
        
    dist = |A*x_p + B*y_p + C| / sqrt(A^2 + B^2)
    
    where A = slope = dy/dx, B = -1, C = intercept = y-slope*x

    """
    A = slope
    B = -1
    C = intercept
     
    dist= abs(A*p[0] + B*p[1] + C) / np.sqrt(A**2 + B**2)
    
    return dist