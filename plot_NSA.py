# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:03:50 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_NSA(img, slope_shaft_axis, intercept_shaft_axis, slope_neck_axis, 
             intercept_neck_axis, name=None, outputfolder=None):
    """
    This function visualizes the neck shaft axis. The resulting plot is saved  
    in the outputfolder or visualized in the plots window.

    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    slope_shaft_axis : float
        The slope of the femoral neck axis.
    intercept_shaft_axis : float
        The intercept of the femoral neck axis.
    slope_neck_axis : float
        The slope of the femoral neck axis.
    intercept_neck_axis : float
        The intercept of the femoral neck axis.
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
    # Plot shaft axis
    axes = plt.gca()
    y_val = np.array(axes.get_ylim())
    y_vals = np.array([0.1*y_val[0], 0.9*y_val[0]])
    x_vals = (y_vals - intercept_shaft_axis) / slope_shaft_axis
    plt.plot(x_vals, y_vals, 'mediumspringgreen', lw=1)
    # Plot neck axis
    x_val = np.array(axes.get_xlim())
    x_vals = np.array([0.2*x_val[1], 0.7*x_val[1]])
    y_vals = slope_neck_axis*x_vals + intercept_neck_axis
    plt.plot(x_vals, y_vals, 'mediumspringgreen', lw=1)
    plt.axis('off')
    if name != None:
        plt.ioff()
        plt.savefig(os.path.join(outputfolder, name+'_NSA.png'))
        plt.close()
        
    return
