# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:58:58 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

def calc_EI(lfh, mfh, p_AE, pts, hip_side_right=True):
    """
    This function calculates the extrusion index (EI) based on the most
    medial point on the femoral head (mfh), the most lateral point of the 
    femoral head (lfh) and the most lateral bony point of the acetabulum (AE).

    Parameters
    ----------
    lfh : array of int
        The indices of the points on the lateral side of the 
        femoral head, 1D array.
    mfh : array of int
        The indices of the points on the medial side of the 
        femoral head, 1D array.
    p_AE : array of float
        The x- and y-coordinates of the most lateral bony point of the 
        acetabulum, 1D array.
    pts : array of float
        The x- and y-coordinates of all the landmark points, 2D array.
    hip_side_right : boolean, optional
        Indicates for which hip side the EI is calculated, the value is True
        for the right hip. The default is 'True'.

    Returns
    -------
    EI : float
        Extrusion index.
    EI_x0 : float
        x-coordinate of the most lateral point of the femoral head.
    EI_x1 : float
        x-coordinate of the most lateral boney point of the acetabulum.
    EI_x2 : float
        x-coordinate of the most medial point of the femoral head.

    """
    
    x_lfh = []
    for index in lfh:
        x_lfh.append(pts[index,0])
    
    x_mfh = []
    for index in mfh:
        x_mfh.append(pts[index,0])
    
    if hip_side_right is True:
        EI_x0 = min(x_lfh)
        EI_x1 = p_AE[0]
        EI_x2 = max(x_mfh)
    else:
        EI_x0 = max(x_lfh)
        EI_x1 = p_AE[0]
        EI_x2 = min(x_mfh)
    
    
    EI = (EI_x1 - EI_x0) / (EI_x2 - EI_x0) * 100
    
    return EI, EI_x0, EI_x1, EI_x2








