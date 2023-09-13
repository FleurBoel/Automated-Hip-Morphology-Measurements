# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 08:32:21 2022

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from skimage.filters import threshold_multiotsu
from skimage.morphology import closing, square


def closest_point(p1, pts):
    """
    This functions identifies the closest point to point p1 from a list of 
    points (pts).

    Parameters
    ----------
    p1 : array of float
        The x- and y-coordinates of point p1, 1D array.
    pts : array of float
        The x- and y-coordinates of all potential points, 2D array.

    Returns
    -------
    pt : array of float
        The x- and y-coordinates of the closest point to point p1 
        from all potential points (pts).

    """
    # Calculate the distance between each potential point and the point p1
    dists = []
    for p2 in pts:
        dists.append(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2))
    
    # Find the closest point
    indx = np.argmin(dists)
    pt = pts[indx]
    
    return pt


def calc_shaft_axis_pelvic(img, p_TMI, p_IC, otsu_levels=3, otsu_thres=1,
                    hip_side_right=True, plot=False):
    """
    This function calculates the shaft axis based on the input image. The 
    cortical bone of the femoral midshaft is segmented using multi-otsu
    thresholding and the midpoint between the lateral and medial cortical 
    bone is defined as the shaft axis using linear regression.
    Note: shaft axis calculation can only be performed is some shaft below 
    the minor trochanter is still visible.

    Parameters
    ----------
    img : array of float
        Matrix containing the image pixel array.
    p_TMI : array of float
        The x- and y-coordinates of the inferior point of the minor 
        trochanter, 1D array.
    p_IC : array of float
        The x- and y-coordinates of the most caudal point of the 
        ischium, 1D array.
    otsu_levels : int, optional
        Number of classes used in the multi-otsu thresholding. The default is 3.
    otsu_thres : int, optional
        Indicate which class threshold value of the multi-otsu thresholding 
        is used to create the segmentation mask. The default is 1.
    hip_side_right : boolean, optional
        Indicates for which hip side the shaft axis is determined, the value 
        is True for the right hip. The default is 'True'.
    plot : boolean, optional
        Indicates whether a plot needs to be generated showing the results
        of the shaft axis calculation. If True an overlay image will be 
        created visualizing the lateral and medial shaft points and the 
        resulting shaft axis. The default is False.
        

    Returns
    -------
    sa_slope : float
        The slope of the femoral neck axis.
    sa_intercept : float
        The intercept of the femoral neck axis.
    """
    # Shaft axis
    # Crop the image below minor trochantor
    tm_cut = round(p_TMI[1])
    ic_cut = round(p_IC[0])
    
    if hip_side_right is True:
        img_c = img[tm_cut:np.size(img, axis=0), 0:ic_cut]
    else:
        img_c = img[tm_cut:np.size(img, axis=0), ic_cut:np.size(img, axis=1)]
    
    # Segment image using multi-otsu segmentation to detect the cortical 
    # bone of the femoral midshaft
    thres = threshold_multiotsu(img_c, otsu_levels)
    mask_otsu = np.asarray(img_c) > thres[otsu_thres]

    # Using morphological operations to clean up the segmentation results
    masked_img = closing(mask_otsu, square(5))
    
    indices_first = []
    indices_last = []
    # Get first and last non-zero argument in each image row
    for row in masked_img:
        indices_first.append((row!=0).argmax(axis=0))
        row_r = np.flip(row)
        indx = (row_r!=0).argmax(axis=0)
        indices_last.append(len(masked_img[0])-indx)
    
    # Create medial points from x and y variables
    pts_m = []
    for i, x_pt in enumerate(indices_last):
        pts_m.append(np.array([x_pt, i]))
    pts_m = np.array(pts_m)
    
    # Create lateral points from x and y variables
    pts_l = []
    for i, x_pt in enumerate(indices_first):
        pts_l.append(np.array([x_pt, i]))
    pts_l = np.array(pts_l)
    
    # Find closest point on medial side for each point on lateral side 
    # and termine the midpoint
    midpoints = []
    for p_l in pts_l:
        # Find closest point on the medial side of the shaft
        p_m = closest_point(p_l, pts_m)
        # Determine midpoint between points
        midpoint = np.array([(p_l[0]+p_m[0])/2, (p_l[1]+p_m[1])/2+tm_cut])
        midpoints.append(midpoint)
        
    midpoints = np.array(midpoints)
    
    
    # Cut-off midpoints to remove outliers
    adj_midpoints = []
    for pt in midpoints:
        if abs(pt[0]-np.mean(midpoints[:,0])) < 0.1*np.mean(midpoints[:,0]):
            adj_midpoints.append(pt)       
    adj_midpoints = np.array(adj_midpoints)
    
    # Generate linear regression line through midpoints, this is the shaft axis
    [sa_slope, sa_intercept] = np.polyfit(adj_midpoints[:,0], adj_midpoints[:,1], 1)
        
    if plot is True:
        # Visualize shaft-axis
        plt.figure(dpi=300)
        plt.imshow(img, cmap = 'gray')
        plt.scatter(pts_l[:,0], pts_l[:,1]+tm_cut, s=0.5, color='cornflowerblue')
        plt.scatter(pts_m[:,0], pts_m[:,1]+tm_cut, s=0.5, color='cornflowerblue')
        plt.scatter(adj_midpoints[:,0], adj_midpoints[:,1], s=0.5, color='red')
        axes = plt.gca()
        y_val = np.array(axes.get_ylim())
        y_vals = np.array([0, y_val[0]])
        x_vals = (y_vals - sa_intercept) / sa_slope
        plt.plot(x_vals, y_vals, 'springgreen')
        plt.axis('off')
        plt.show()
        
    return sa_slope, sa_intercept

    

        
    
    
    
    

    
    