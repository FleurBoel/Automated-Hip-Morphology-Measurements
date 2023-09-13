# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 08:38:19 2022

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
from angle_3_points import angle_3_points


def calc_CEA(c_x, c_y, p_a, hip_side_right=True):
    """
    This function calculates the center edge angle based on the femoral head 
    center and the point on the acetabulum in degrees. No correction is 
    applied with regards to the horizontal reference line of the pelvis.
    
    Parameters
    ----------
    c_x : float
        x-coordinate of the femoral head center.
    c_y : float
        y-coordinate of the femoral head center.
    p_a : array of float
        The x- and y-coordinates of the most lateral part of the sourcil
        (CEA of Wiberg) or the most lateral point of the bony acetabulum 
        (lateral CEA).
    hip_side_right : boolean, optional
        Indicates for which hip side the CEA is calculated, the value is True
        for the right hip. The default is 'True'.

    Returns
    -------
    cea : float
        The center edge angle in degrees.

    """
    # Define the points forming the CEA
    cea_p0 = np.array([c_x, c_y-1])
    cea_p1 = np.array([c_x, c_y])
    cea_p2 = p_a
    
    cea_uncorr = angle_3_points(cea_p0, cea_p1, cea_p2, degree=True)
    
    # Correction if angle is negative, e.i. the most lateral point of the 
    # acetubulum is medial of the fermoral head center.
    if hip_side_right is True:
        if c_x > p_a[0]:
            cea = cea_uncorr
        else: cea = -cea_uncorr
    else:
        if c_x < p_a[0]:
            cea = -cea_uncorr
        else: cea = cea_uncorr
    
    return cea