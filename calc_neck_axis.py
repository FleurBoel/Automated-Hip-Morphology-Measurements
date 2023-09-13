# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:06:06 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np

def calc_neck_axis(ln_pts, mn_pts, c_fh):
    """
    This function calculates the logitudinal axis of the neck.

    Parameters
    ----------
    ln_pts : array of float
        The x- and y-coordinates of all lateral neck points.
    mn_pts : array of float
        The x- and y-coordinates of all medial neck points.
    c_fh : array of float
        Femoral head center, 1D array.

    Returns
    -------
    c_n : array of float
        The x- and y-coordinates of the femoral neck center, 1D array.
    na_slope : float
        The slope of the femoral neck axis.
    na_intercept : float
        The intercept of the femoral neck axis.

    """
    # Center of the femoral neck
    n_pts = []
    for lateral in ln_pts:
        for medial in mn_pts:
            n_xy = np.zeros([1,2])
            n_xy[0,0] = (medial[0] + lateral[0])/2
            n_xy[0,1] = (medial[1] + lateral[1])/2
            n_pts.append(n_xy)
    
    # Calculate mean, which is the neck center
    c_n = np.mean(n_pts, axis=0)
    c_n = c_n.flatten()
    # Longitudinal axis of the neck
    # Get slope
    na_slope = (c_n[1] - c_fh[1]) / (c_n[0] - c_fh[0])
    # Get intercept for neck axis
    na_intercept = c_fh[1] - na_slope*c_fh[0]
    
    return c_n, na_slope, na_intercept