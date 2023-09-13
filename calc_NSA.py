# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:06:06 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import math
import numpy as np


def calc_NSA(slope_shaft_axis, slope_neck_axis, degree=True):
    """
    This function calculates the neck shaft angle based on the slope of the 
    shaft axis and the slope of the neck axis.

    Parameters
    ----------
    slope_shaft_axis : float
        Slope of the shaft axis.
    slope_neck_axis : float
        Slope of the neck axis.
    degree : boolean, optional
        Indicates if the resulting angle will be calculated in degrees (True)
        or radians (False). The default is 'True'.

    Returns
    -------
    NSA : float
        The neck shaft angle.

    """
    
    NSA_uncorr = math.atan(abs((slope_neck_axis-slope_shaft_axis)/(1+slope_shaft_axis*slope_neck_axis)))
    
    if degree is False:
        NSA = np.pi - NSA_uncorr
    else: NSA = 180 - np.degrees(NSA_uncorr)
    
    return NSA