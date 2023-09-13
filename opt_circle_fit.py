# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 12:13:41 2022

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
from circle_fit import circle_fit

def opt_circle_fit(c_points, pts):
    """
    This function finds the best-fitting circle based on the given points and
    indices. Nine different circles are fitted based on nine different 
    combinations of points in order to optimize the circle fit. The best-fitting
    circle is chosen as the circle with the smallest error and the smallest
    radius. If these circles are not the same, an even trade-off is made 
    between these characteristics.
    
    Parameters
    ----------
    c_points : array of float
        The indices of the circle points for which the best-fitting circle 
        needs to be determined.
    pts : array array of float
        The x- and y-coordinates of of all landmark points of the hip, 2D array.

    Returns
    -------
    c_values : list
        List containing the x-coordinate, y-coordinate and radius of the
        best-fitting circle.
    c_val_pts : array
        The x- and y-coordinates of the points used to obtain the 
        best-fitting circle.
    """
    
    # Create best-fitting circle with multiple combinations of the femoral head
    # points and select the circle fit with the smallest RMSE.
    
    # Obtain x- and y-coordinates of the points used to find the best fitting 
    # circle
    c_pts = []
    for i in c_points:
        c_pts.append(pts[i,:])
    
    # Create nine different variations by removing points on the lateral and
    # medial side of the femoral head.
    
    # 13 year olds
    opt_c_pts = [c_pts, c_pts[1:len(c_pts)], c_pts[0:-1], c_pts[0:-2],  
                 c_pts[2:len(c_pts)], c_pts[1:-1], c_pts[1:-2], 
                 c_pts[2:-1], c_pts[2:-2]]
    
    
    # Determine the circle fit using the circle_fit function, which returns
    # the x-coordinate, y-coordinate and radius of the best-fitting circle and 
    # the RMSE error of the fit.
    cf_x = []
    cf_y = []
    cf_r = []
    cf_error = []
    for i in range(len(opt_c_pts)):
        
        # Find the best-fitting circle for each combination of points
        c_points = np.array(opt_c_pts[i])
        [c_x, c_y, c_r, error] = circle_fit(c_points)
        
        # Store circle parameters
        cf_x.append(c_x)
        cf_y.append(c_y)
        cf_r.append(c_r)
        cf_error.append(error)
    
    # Sort both the error and the radius from smallest to largest
    sort_err = np.argsort(np.argsort(cf_error))
    sort_r = np.argsort(np.argsort(cf_r))
    
    # Trade off between smallest error and smallest radius
    sort = sort_err + sort_r
    small = np.argmin(sort)
    
    # Get circle values for selected circle fit
    c_values = [cf_x[small], cf_y[small], cf_r[small]]
    c_val_pts = np.array(opt_c_pts[small])
    
    return c_values, c_val_pts