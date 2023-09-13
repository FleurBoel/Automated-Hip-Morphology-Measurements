# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:39:23 2022

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
from angle_3_points import angle_3_points


def calc_AI(p_AE, p_TC, p_H=None, hip_side_right=True):  
    """
    This function calculates the acetabular index based on the most lateral 
    point of the bony acetabulum and the most lateral point of the triradiate 
    cartilage.
    
    Parameters
    ----------
    p_AE : array of float
        The x- and y-coordinates of the most lateral bony point of the 
        acetabulum, 1D array.
    p_TC : array of float
        The x- and y-coordinates of the most lateral point of the triradiate 
        cartilage, 1D array.        
    p_H : array of float, optional
        The x- and y-coordinates of a point along the horizontal reference  
        line of the pelvis through point p_TC, 1D array. If none is indicated, 
        the horizontal reference line is assumed to be parallel to the
        horizontal axis of the image. The default is None.
    hip_side_right : boolean, optional
        Indicates for which hip side the AI is calculated, the value is True
        for the right hip. The default is 'True'.

    Returns
    -------
    ai : float
        Acetabular index in degrees.

    """
    
    # If p_H is not provided, the angle is calculated in relation to the 
    # horizontal axis of the image
    if p_H is None:
        if hip_side_right is True:
            p_H = p_TC - np.array([10,0])
        else: p_H = p_TC + np.array([10,0])
    
    
    ai_uncorr = angle_3_points(p_AE, p_TC, p_H, degree=True)
    
    # Correction if the AI needs to be negative, e.i. the most lateral point  
    # of the acetubulum is lower than the most lateral point of the 
    # triradiate cartilage.
    if p_AE[1] > p_TC[1]:
        ai = -ai_uncorr
    else: ai = ai_uncorr
   
    
    return ai