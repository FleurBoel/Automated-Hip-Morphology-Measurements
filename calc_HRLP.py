# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 08:26:01 2022

@author: Fleur Boel, f.boel@erasmusmc.nl
"""
from angle_3_points import angle_3_points
from statistics import mean

def corr_HRLP(pt_LH, pt_RH, angle):
    """
    Correct the found horizontal reference line of the pelvis (HRLP) angle 
    based on the relationship between the left and right hip points.     
    If the HRLP is downward the resulting angle should be negative.
    The HRLP is downward if the RIGHT hip point is located more cranial than
    the LEFT hip point. NOTE: the origin of the image is at the top left
    hand corner of the image.
    
    Parameters
    ----------
    pt_LH : array of float
        The x- and y-coordinates of the point of the left hip.
    pt_RH : array of float
        The x- and y-coordinates of the point of the right hip. 
    angle : float
        The uncorrected angle of the horizontal reference line of the pelvis 
        (HRLP) in degrees.

    Returns
    -------
    corr_angle : float
        The corrected angle of the horizontal reference line of the pelvis 
        (HRLP) in degrees.

    """
    
    if pt_LH[1] > pt_RH[1]:
        corr_angle = -angle
    else: corr_angle = angle
    
    return corr_angle



def calc_HRLP(io_points, pts_LH, pts_RH):
    """
    Determine the horizontal reference line of the pelvis (HRLP)
    in degrees based on Ischium (0) and Obturator foramen(1), if the HRLP
    is downward, the value of the angle will be negative

    Parameters
    ----------
    io_points : array of int
        The indices of the points on the most caudal point of the ischium and
        the superolateral corner of the obturator foramen, 1D array.
    pts_LH : array of float
        The x- and y-coordinates of all the landmark points of the left hip.
    pts_RH : array of float
        The x- and y-coordinates of all the landmark points of the right hip.
    
    Returns
    -------
    hrlp_angle : float
        The angle of the horizontal reference line of the pelvis (HRLP) in degrees.

    """
    
    # Calc HRLP based on io points
    hrlp_angles = []
    for point in io_points:
        # get point coordinats
        io_pts_LH = pts_LH[point,:]
        io_pts_RH = pts_RH[point,:]
        
        # Calc angle
        hrlp_io = angle_3_points(io_pts_LH, io_pts_RH, degree=True)
        
        # Perform correction
        hrlp_angles.append(corr_HRLP(io_pts_LH, io_pts_RH, hrlp_io))
    
    
    # Get mean
    hrlp_angle = mean(hrlp_angles) 
    
    return hrlp_angle