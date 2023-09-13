# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:32:39 2023

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_EI(img, EI_x0, EI_x1, EI_x2, c_vals, name=None, outputfolder=None):
    """
    This function visualizes the extrusion index. The resulting plot is saved  
    in the outputfolder or visualized in the plots window.

    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    EI_x0 : float
        x-coordinate of the most lateral point of the femoral head.
    EI_x1 : float
        x-coordinate of the most lateral bony point of the acetabulum.
    EI_x2 : float
        x-coordinate of the most medial point of the femoral head.
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
    
    # Create image and save
    plt.figure(dpi=300)
    plt.imshow(img, cmap='gray')
    # Plot vertical lines
    plt.vlines(x = [EI_x0, EI_x1, EI_x2], ymin = c_vals[1] - c_vals[2], ymax = c_vals[1] + c_vals[2],
           colors = 'mediumspringgreen', lw=1)
    # Plot horizontal line to connect
    plt.plot(np.array([EI_x0, EI_x2]), 
                 np.array([c_vals[1], c_vals[1]]), 'mediumspringgreen', lw=1)
    plt.axis('off')
    if name != None:
        plt.ioff()
        plt.savefig(os.path.join(outputfolder, name+'_EI.png'))
        plt.close()
        
    return