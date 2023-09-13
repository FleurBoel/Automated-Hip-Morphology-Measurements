# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:06:06 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

from dist_measures import perp_dist, dist_2_points

def calc_ADR(p_AS, p_AE, p_TD):
    """
    This function calculates the acetabular depth-width ratio.

    Parameters
    ----------
    p_AS : array of float
        The x- and y-coordinates of the most medial point of the acetabular 
        sourcil, 1D array.
    p_AE : array of float
        The x- and y-coordinates of the most lateral bony point of the 
        acetabulum, 1D array.
    p_TD : array of float
        The x- and y-coordinates of the most inferior point of the teardrop, 
        1D array.

    Returns
    -------
    ADR : float
        The acetabular depth-width ratio.

    """
    
    dist_A = perp_dist(p_AS, p_AE, p_TD)
    dist_B = dist_2_points(p_AE, p_TD)

    ADR = dist_A / dist_B *1000
    
    return ADR
