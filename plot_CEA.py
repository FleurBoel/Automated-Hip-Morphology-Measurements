# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:16:38 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_CEA(img, c_vals, p_A, angle_HRLP, name=None, outputfolder=None):
    """
    This function visualizes the center edge angle based on the femoral head 
    center and the point on the acetabulum. The resulting plot is saved in 
    the outputfolder or visualized in the plots window.

    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    c_vals : list
        List containing the x-coordinate, y-coordinate and radius of the
        best fitting circle.
    p_A : array of float
        The x- and y-coordinates of the most lateral part of the sourcil
        (CEA of Wiberg) or the most lateral point of the bony acetabulum 
        (lateral CEA).
    angle_HRLP : float
        The angle of the horizontal reference line of the pelvis (HRLP) in degrees.
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
    
    # Adjust the horizontal reference line of the pelvis (HRLP) for 
    # the fact that the origin is at the top left of the image
    slope_hrlp = np.tan(np.deg2rad(360-angle_HRLP))
    
    # Create image and save
    plt.figure(dpi=300)
    plt.imshow(img, cmap='gray')
    # Plot best fitting circle
    circle = plt.Circle((c_vals[0], c_vals[1]), c_vals[2], fill=False, color='k', lw=0.5)
    plt.gca().add_patch(circle)
    # Plot horizontal reference line of the pelvis (HRLP)
    plt.axline(([c_vals[0], c_vals[1]]), slope = slope_hrlp, 
               color='mediumspringgreen', lw=1)
    # Plot line 1 perpendicular to HRLP
    slope_A = -1/slope_hrlp
    intercept_A = c_vals[1] - slope_A*c_vals[0]
    y_vals = np.array([c_vals[1], c_vals[1]-1.5*c_vals[2]])
    x_vals = (y_vals - intercept_A) / slope_A
    plt.plot(x_vals, y_vals, 'mediumspringgreen', lw=1)
    # Plot line 2 through femoral head center and point acetabulum
    plt.plot(np.array([p_A[0], c_vals[0]]), 
                 np.array([p_A[1], c_vals[1]]), 'mediumspringgreen', lw=1)
    plt.axis('off')
    if name != None:
        plt.ioff()
        plt.savefig(os.path.join(outputfolder, name+'_CEA.png'))
        plt.close()
        
    return