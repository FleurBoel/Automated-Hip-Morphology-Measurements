# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 12:58:23 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_AI(img, p_AE, p_TC, angle_HRLP, name=None, outputfolder=None):
    """
    This function visualizes the acetabular index based on the most lateral 
    point of the bony acetabulum, the most lateral point of the triradiate 
    cartilage and the horizontal reference line of the pelvis (HRLP). 
    The resulting plot is saved in the outputfolder or visualized in the
    plots window.
    
    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    p_AE : array of float
        The x- and y-coordinates of the most lateral bony point of the 
        acetabulum, 1D array.
    p_TC : array of float
        The x- and y-coordinates of the most lateral point of the triradiate 
        cartilage, 1D array.
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
    
    # Create image and save
    plt.figure(dpi=300)
    plt.imshow(img, cmap='gray')
    # Plot line 1
    # Adjust the horizontal reference line of the pelvis (HRLP) for 
    # the fact that the origin is at the top left of the image
    slope_hrlp = np.tan(np.deg2rad(360-angle_HRLP))
    plt.axline(([p_TC[0], p_TC[1]]), slope = slope_hrlp, 
               color='mediumspringgreen', lw=1)
    # Plot line 2
    plt.plot(np.array([p_AE[0], p_TC[0]]), 
                 np.array([p_AE[1], p_TC[1]]), 'mediumspringgreen', lw=1)
    plt.axis('off')
    if name != None:
        plt.ioff()
        plt.savefig(os.path.join(outputfolder, name+'_AI.png'))
        plt.close()
    
    return