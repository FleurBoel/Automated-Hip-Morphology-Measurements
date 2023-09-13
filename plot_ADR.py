# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:11:19 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_ADR(img, p_AS, p_AE, p_TD, name=None, outputfolder=None):
    """
    This function visualizes the acetabular depth-width ratio. The resulting 
    plot is saved in the outputfolder or visualized in the plots window.

    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    p_AS : array of float
        The x- and y-coordinates of the most medial point of the acetabular 
        sourcil, 1D array.
    p_AE : array of float
        The x- and y-coordinates of the most lateral bony point of the 
        acetabulum, 1D array.
    p_TD : array of float
        The x- and y-coordinates of the most inferior point of the teardrop, 
        1D array.
    name : str, optional
        String containing the name which will be used to save the file. The 
        default is None.
    outputfolder : WindowsPath, optional
        Windows path to the folder where the images will be saved. The default 
        is None.

    Returns
    -------
    None.

    """
    
    # Create image and save
    plt.figure(dpi=300)
    plt.imshow(img, cmap = 'gray')
    # Line B
    plt.plot(np.array([p_AE[0], p_TD[0]]), 
             np.array([p_AE[1], p_TD[1]]), 'mediumspringgreen', lw=1)
    slope_B = (p_TD[1]-p_AE[1])/(p_TD[0]-p_AE[0])
    intercept_B = p_TD[1] - slope_B*p_TD[0]
    # Line A
    slope_A = -1/slope_B
    intercept_A = p_AS[1] - slope_A*p_AS[0]
    # Intersect line A and B
    x_val = (intercept_B - intercept_A) / (slope_A - slope_B)
    y_val = slope_A*x_val + intercept_A
    plt.plot(np.array([p_AS[0], x_val]), 
             np.array([p_AS[1], y_val]), 'mediumspringgreen', lw=1)
    plt.axis('off')
    if name != None:
        plt.ioff()
        plt.savefig(os.path.join(outputfolder, name+'_ADR.png'))
        plt.close()
    
    return
