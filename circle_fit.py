# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 08:21:46 2021

Hyper circle fit

@author: Fleur Boel, f.boel@erasmusmc.nl
"""

import numpy as np
import math
import scipy.linalg

def circle_fit(points, epsilon = 10**-12):
    """
    Algebraic circle fit: Hyper fit
    
    Parameters
    ----------
    points : array of float
        The x- and y-coordinates of the points to which the circle
        needs to be fitted, 2D array.
    epsilon : float, optional
        Tolerance. The default epsilon is 10^-12.
    

    Returns
    -------
    c_x : float
        The x-coordinate of the circle center
    c_y : float
        The y-coordinate of the circle center
    r : float
        Radius of the circle
    error : float
        Root mean square error (RSME) of the circle fit
        
    A. Al-Sharadqah, N. Chernov. Error analysis for circle fitting algorithms. 
    Electron J Stat. 2009;3:886-911.
    """
    
    # Translate coordinate system to centroid of the data set, simplifies the
    # computation of inv(H)
    ctrd = np.array([np.mean(points[:,0]), np.mean(points[:,1])])
    X = points[:,0]-ctrd[0]
    Y = points[:,1]-ctrd[1]
    
    # Compute datamatrix Z
    z = X*X + Y*Y
    Z = np.array([z, X, Y, np.full((len(z)), 1)]).T

    # Compute Singular value decomposition (svd)
    [U, Sdiag, Vt] = np.linalg.svd(Z)
    
    # Find parameter vector A
    if min(Sdiag) < epsilon:
        A = Vt.T[:,3]
    else:
        # Compute matrix Sigma from Sdiag (contains the non-zero sigular values)
        if Z.shape[0] > Z.shape[1]:
            sigma = np.zeros((Z.shape[1], Z.shape[1]))
        else:
            sigma = np.zeros((Z.shape[0], Z.shape[1]))

        sigma[:min(Z.shape[0],Z.shape[1]), :min(Z.shape[0],Z.shape[1])] = np.diag(Sdiag)
    
        # Compute Y = V*Sigma*V.T
        W = Vt.T @ sigma @ Vt
    
        # Find eigenvalues and eigenvectors of Y*inv(H)*Y
        R = np.array([np.mean(Z[:,0]), np.mean(Z[:,1]), np.mean(Z[:,2])])
        H = np.array([[8*R[0], 4*R[1], 4*R[2], 2], [4*R[1], 1, 0, 0], 
                      [4*R[2], 0, 1, 0], [2, 0, 0, 0]])
        [evals, evecs] = scipy.linalg.eigh(W @ np.linalg.inv(H) @ W)
    
        # Select eigenpair (eta, A_star) with smallest positive eigenvalue
        A_star = evecs[:,1]
    
        # Compute parameter vector A, A = Y.T*A_star
        A = np.linalg.inv(W) @ A_star

    # Compute circle parameters, translated to image data
    c_x = -1*A[1] / (2*A[0]) + ctrd[0]
    c_y = -1*A[2]/ (2*A[0]) + ctrd[1]
    r = np.sqrt(A[1]*A[1]+A[2]*A[2]-4*A[0]*A[3])/(2*abs(A[0]));
    
    # Compute RSME 
    dist = []
    # Get distance from point to circle (interpret as y - y_hat)
    for point in points:
        dist.append(abs(math.dist(point, np.array([c_x, c_y]))-r))
    # Calculate RMSE
    error = np.sqrt(np.square(dist).mean())
    
    return c_x, c_y, r, error