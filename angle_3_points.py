# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:37:05 2022

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import math

def angle_3_points(p0, p1=np.array([0,0]), p2 = None, degree = True):
    """
    This function calculates the angle p0p1p2.
    
    Parameters
    ----------
    p0 : array of float
        The x- and y-coordinates of p0, 1D array.
    p1 : array of float, optional
        The x- and y-coordinates of p1, 1D array. The default is np.array([0,0]).
    p2 : array of float, optional
        The x- and y-coordinates of p2, 1D array. The default is None.
    degree: boolean, optional
        Indicates whether the angle should be calculated in degree (True) 
        or radians (False). The default is 'True'.
        
    Returns
    -------
    angle : float
        Angle or corner p0p1p2.
        
    James W. Walker. (2016) Computing Angle Between Vectors. 
    url: https://www.jwwalker.com/pages/angle-between-vectors.html
    """
    # If p2 is not provided, the angle is calculated in relation to the 
    # horizontal axis of the image.
    if p2 is None:
        p2 = p1 + np.array([1,0])
    
    # Constuct vectors v0 and v1
    v0 = np.array(p0-p1)
    v1 = np.array(p2-p1)
    
    # Angle = atan2(crossproduct(v0, v1), dotproduct(v0, v1))
    angle_rad = math.atan2(np.linalg.norm(np.cross(v0, v1)), np.dot(v0, v1))
    
    # Convert to degree if needed
    if degree is False:
        angle = angle_rad
    else: angle = np.degrees(angle_rad)
    
    return angle