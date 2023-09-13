# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:06:06 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
from scipy.interpolate import make_interp_spline

def spline_int(fhn_pts, df=1):
    """
    This function determines the interpolating spine through the femoral
    head neck points based on the Scipy
    package.

    Parameters
    ----------
    fhn_pts : array of float
        The x- and y-coordinates of all lateral femoral head and neck points 
        up to and including the most superior point of the femoral head.
    df: int, optional
        The degrees of freedom used to fit the BSpline object. The default is 1.

    Returns
    -------
    spl : scipy.interpolate._bsplines.BSpline
        A BSpline object of the degree k=df.
    x_int : array of float
        x-values used for fitting the b-spline.
    y_int : array of float
        y-values used for fitting the b-spline.

    """
    # Flip arrays of the coordinates to set the y-values in ascending order.
    y_int = np.flip(fhn_pts[:,1])
    x_int = np.flip(fhn_pts[:,0])
    
    # Make sure y_int is in ascending order, which is needed for the Scipy 
    # make_interp_spline function. This removes any neck points beyond the
    # lowest point on the lateral femoral neck.
    y_int = y_int[0:np.argmax(y_int)+1]
    x_int = x_int[0:np.argmax(y_int)+1]
    
    # Create spline using y-values.
    spl = make_interp_spline(y_int, x_int, k=df)
    
    return spl, x_int, y_int