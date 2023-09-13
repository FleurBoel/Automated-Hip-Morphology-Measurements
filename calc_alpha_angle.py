# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:06:06 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
from angle_3_points import angle_3_points
from spline_int import spline_int

def calc_alpha_angle(fhn_pts, c_vals, c_n, error_margin_points=1.04, 
                     error_margin_spline=1, degree=True):
    """
    This function calculates the alpha angle based on the femoral head neck 
    points and the best-fitting circle around the femoral head. If non of the 
    femoral head neck points are ouside of the best-fitting circle, the 
    function will return the string "NaN" for the alpha angle.

    Parameters
    ----------
    fhn_pts : array of float
        Array containing the x- and y-coordinates of all lateral femoral head
        and neck points, 2D array
    c_vals : list
        List containing the x-coordinate, y-coordinate and radius of the
        best-fitting circle.
    c_n : array of float
        The x- and y-coordinates of the femoral neck center, 1D array.
    error_margin_points : float, optional
        The error margin to determine when a point is outside
        of the best-fitting circle. This limit is based on the 
        radius of the best-fitting circle. The default is 1.04 times the radius.
    error_margin_spline : float, optional
        The error margin to determine when the spline is outside
        of the best-fitting circle. This limit is based on the 
        radius of the best-fitting circle. The default is 1 times the radius.
    degree: boolean, optional
        Indicates if the resulting angle will be calculated in degrees (True)
        or radians (False). The default is 'True'.

    Returns
    -------
    alpha_angle : float
        The alpha angle.
    ap : array of float
        The coordinates of the found alpha point, 1D array.

    """
    
    # Select superiolateral femoral head points and neck points
    # Select fhn_points up to and including most superior point femoral head
    fhn_pts_aa = fhn_pts[0:np.argmin(fhn_pts[:,1])+1, :]
    
    # Calculate distance between femoral head neck pts and center femoral head
    dist = []
    for lateral in fhn_pts_aa:
        dist.append(np.sqrt((lateral[0]-c_vals[0])**2 + (lateral[1]-c_vals[1])**2))
        
    
    # Set the limit at a margin based on the radius of the best-fitting circle
    limit = c_vals[2]*error_margin_points
    # Check if any of the points are outside of the best-fitting circle
    if sum(dist >= limit) > 0:
        # Find all point indices which are outside of the best-fitting circle
        indices = np.flatnonzero(dist >= limit)
        
        # Check to see if indices are consecutive, meaning the femoral head
        # leaves the best-fitting circle and does not return inside the circle.
        for i, indx in enumerate(indices):
            conseq = True
            if indx != i:
                conseq = False
                break
        
        # If the indices are consecutive: the alpha point is around the last 
        # index in the row
        if conseq is True:
            index = indices[-1]   
        # If the indices are NOT consecutive, at what point do the points
        # definitivaly leave the best-fitting circle --> we assume that with 
        # a cam deformity, the femoral head stays outside the best-fitting
        # circle.
        else:
            for i, indx in enumerate(indices):
                if indx != i:
                    index = indices[i-1]
                    break
        
        # Find alpha point on interpolated curve
        # Interpolate between landmark points using b-splines
        [spl_y, xint, yint] = spline_int(fhn_pts_aa)
        
        
        # Point before and after index point are taken into account
        if index == 0:
            if fhn_pts_aa[index+2,1] < fhn_pts_aa[index,1]:
                yspl = np.arange(fhn_pts_aa[index+2,1], fhn_pts_aa[index,1], 0.01)
            else: yspl = np.arange(fhn_pts_aa[index+1,1], fhn_pts_aa[index,1], 0.01)
        elif index == len(fhn_pts_aa)-1:
            if fhn_pts_aa[index,1] < fhn_pts_aa[index-2,1]:
                yspl = np.arange(fhn_pts_aa[index,1], fhn_pts_aa[index-2,1], 0.01)
            else: yspl = np.arange(fhn_pts_aa[index,1], fhn_pts_aa[index-1,1], 0.01)
        else: 
            if fhn_pts_aa[index+1,1] < fhn_pts_aa[index-1,1]:
                yspl = np.arange(fhn_pts_aa[index+1,1], fhn_pts_aa[index-1,1], 0.01)
            else: yspl = np.arange(fhn_pts_aa[index+1,1], fhn_pts_aa[index,1], 0.01)
        
        xspl = spl_y(yspl)
        
        # Calculate distance between the interpolated points and the center 
        # of the femoral head
        dist_spl = []
        count_dis = 0
        for x in xspl:
            dist_spl.append(np.sqrt((x-c_vals[0])**2 + (yspl[count_dis]-c_vals[1])**2))
            count_dis+=1
                
        # Set the limit at a margin based on the radius of the best-fitting circle
        limit_spl = c_vals[2]*error_margin_spline
        # Check if any of the points are outside of the best-fitting circle
        if sum(dist_spl >= limit_spl) > 0:
            # Check at which point the distance is greater than the radius
            indices_spl = np.flatnonzero(dist_spl >= limit_spl)
            # Find incidence at which the points are outside the circle
            index_spl = indices_spl[0]
            # Define the alpha point as the first point that leaves the
            # best-fitting circle
            ap = np.array([xspl[index_spl], yspl[index_spl]])
        else:
            # If no points on the spline are outside the best-fitting circle,
            # the original index point is used
            ap = fhn_pts_aa[index]
            
        # Calculate the alpha angle
        c_h = np.array([c_vals[0], c_vals[1]])
        if degree is True:
            alpha_angle = angle_3_points(ap, c_h, c_n, degree=True)
        else: alpha_angle = angle_3_points(ap, c_h, c_n, degree=False)
        
    
    else: 
        alpha_angle = "NaN"
        ap = "NaN"
        
    return alpha_angle, ap