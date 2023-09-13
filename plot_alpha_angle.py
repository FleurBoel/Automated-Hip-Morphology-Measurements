# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:16:08 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_alpha_angle(img, ap, c_n, c_vals, slope_neck_axis, 
                     intercept_neck_axis, name=None, outputfolder=None):
    """
    This function visualizes the alpha angle. The resulting plot is saved 
    in the outputfolder or visualized in the plots window.

    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    ap : array of float
        The x- and y-coordinates of the found alpha point, 1D array.
    c_n : array of float
        The x- and y-coordinates of the femoral neck center, 1D array.
    c_vals : list
        List containing the x-coordinate, y-coordinate and radius of the
        best-fitting circle.
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
    
    # Create image
    plt.figure(dpi=300)
    plt.imshow(img, cmap='gray')
    # Plot best-fitting circle
    circle = plt.Circle((c_vals[0], c_vals[1]), c_vals[2], fill=False, 
                        color='black', lw=1)
    plt.gca().add_patch(circle)
    # Line 1
    plt.plot(np.array([ap[0], c_vals[0]]), 
             np.array([ap[1], c_vals[1]]), 'mediumspringgreen', lw=1)
    # Line 2: neck axis
    axes = plt.gca()
    x_val = np.array(axes.get_xlim())
    x_vals = np.array([0.2*x_val[1], 0.75*x_val[1]])
    y_vals = slope_neck_axis*x_vals + intercept_neck_axis
    plt.plot(x_vals, y_vals, 'mediumspringgreen', lw=1)
    
    plt.axis('off')
    if name != None:
        plt.ioff()
        plt.savefig(os.path.join(outputfolder, name+'_Alpha_angle.png'))
        plt.close()
        
    return
