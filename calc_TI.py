# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:06:06 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
from dist_measures import perp_dist_line, dist_2_points
from spline_int import spline_int

def calc_TI(fhn_pts, c_fn, c_vals, slope_neck_axis):
    """
    This function determines the triangular index based on the femoral head  
    neck points, the femoral neck axis and the best-fitting circle
    around the femoral head.

    Parameters
    ----------
    fhn_pts : array of float
        The x- and y-coordinates of all lateral femoral head and neck points,
        2D array.
    c_fn : array of float
        The x- and y-coordinates of the femoral neck center, 1D array.
    c_vals : list
        List containing the x-coordinate, y-coordinate and radius of the
        best-fitting circle.
    slope_neck_axis : float
        The slope of the femoral neck axis.

    Returns
    -------
    TI : float
        The triangular index.
    H : array of float
        The x- and y-coordinates of point H, which is the point at half the 
        radius from the femoral head center along the neck_axis, 1D array. 
        This point is used to determine the TI.
    S : array of float
        The x- and y-coordinates of point S, which is the intersection of the  
        femoral head and the line through point H perpedicular to the neck 
        axis, 1D array.

    """
    # Select fhn_points up to and including most superior point femoral head
    fhn_pts_ti = fhn_pts[0:np.argmin(fhn_pts[:,1])+1, :]
    
    # Define point H, at distance 0.5*r from femoral head center along the neck axis
    # Vector v is vector from femoral head center to femoral neck center
    c_fh = np.array([c_vals[0], c_vals[1]])
    v = np.array(c_fn-c_fh)
    
    # Unit vector of vector v
    u = v/np.linalg.norm(v)
    
    # Define point H
    H = c_fh + c_vals[2]*0.5*u
    
    # Create line perpendicular to neck axis through point H
    # Perpendicular lines: rc_1 * rc_2 = -1
    # Intercept = y - slope*x
    slope_line_h = -1/slope_neck_axis
    intercept_line_h = H[1] - slope_line_h*H[0]
    
    # Find closest fhn points to point H
    # Calculate distance from all points to point H
    dist = []
    for lateral in fhn_pts_ti:
        dist.append(perp_dist_line(lateral, slope_line_h, intercept_line_h))
    dist = np.array(dist)
        
    # Find shortest two distances
    indices = np.argsort(dist)[:2]
    
    # Find intersection point on interpolated curve
    # Interpolate between landmark points using b-splines
    [spl_y, xint, yint] = spline_int(fhn_pts_ti)
        
    # Find point S
    if fhn_pts_ti[indices[0],1] < fhn_pts_ti[indices[1],1]:
        yspl = np.arange(fhn_pts_ti[indices[0],1], fhn_pts_ti[indices[1],1], 0.01)
    else: yspl = np.arange(fhn_pts_ti[indices[1],1], fhn_pts_ti[indices[0],1], 0.01)
    
    xspl = spl_y(yspl)
    
    # Create 2d array containing point coordinates
    p_spl = np.column_stack((xspl, yspl))
    
    # Get distance from spline points to line and select point with smallest distance
    dist_spl = []
    for point in p_spl:
        dist_spl.append(perp_dist_line(point, slope_line_h, intercept_line_h))
        
    # Get smallest distance, this point is point S
    index = np.argmin(dist_spl)
    
    S = p_spl[index, :]
    
    # Calculate distance point S and the center of the femoral head
    TI = dist_2_points(S, c_fh)
    
    return TI, H, S