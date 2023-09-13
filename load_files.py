# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 15:55:22 2021

@author: Fleur Boel, f.boel@erasmusmc.nl
"""


import numpy as np
import matplotlib.pyplot as plt
import pydicom

def load_point_data(filepath):
    """
    Load the coordinates of the landmark points from the text file and create 
    a 2D numpy array containing the coordinates.
    NOTE: the assumption is made that the coordinates of point 0
    are located on the 3rd line of the textfile.
    
    Parameters
    ----------
    filepath : WindowsPath
        WindowsPath object containing the file path to the text file containing
        the x- and y-coordinates of all the landmark points.

    Returns
    -------
    point_data : array of float
        The x- and y-coordinates of all the landmark points, 2D array

    """
    # Get number of points from file
    NoP = np.loadtxt(filepath, skiprows=1, max_rows=1, usecols=(1))
    NoP = np.int(NoP)
    
    with open(filepath, 'r') as fr:
        lines = fr.readlines()
    NoP_check = len(lines[3:len(lines)-1])
    
    if NoP == NoP_check:
        # Load data, skip first 3 rows, since these don't contain point coordinates
        point_data = np.loadtxt(filepath, skiprows=3, max_rows=NoP)
    else: point_data = []; print('NoP incorrect {}'.format(filepath))
    
    return point_data


def load_image(filepath):
    """
    This function loads the image defined by the file path.
    If the image is a 3-dimensional image, only the first dimension is used.
    The assumption is that all images are grayscale images.

    Parameters
    ----------
    filepath :  WindowsPath
        WindowsPath object containing the file path to the image file.

    Returns
    -------
    img : array of float
        Matrix containing the image pixel array.
    spacing: float
        The pixel spacing of the image file IF a dicom image is loaded,
        otherwise spacing is 0.

    """
    
    if filepath[-3:len(filepath)] == 'dcm' or filepath[-3:len(filepath)] == 'DCM':
        dcm_img = pydicom.dcmread(filepath)
        img = dcm_img.pixel_array
        if hasattr(dcm_img, "PixelSpacing") is True:
            spacing = dcm_img.PixelSpacing[0]
        else: spacing = 0
    else: 
        img = plt.imread(filepath)
        if np.ndim(img) == 3:
            img = img[:,:,0]
        spacing = 0
    
        
    return img, spacing



def read_imglist(imglist, folder_pts, folder_img):
    """
    This function reads the image and pointsfile names from an imagelist 
    and checks if the image and pointsfile exist.
    NOTE: the assumption is made that the first image and pointfile name
    are on the 8th file line.

    Parameters
    ----------
    imglist : WindowsPath
        WindowsPath object containing the file path to the text file containing
        the imagelist.
    folder_pts : WindowsPath
        WindowsPath object containing the filepath to the folder containing
        the pointfiles.
    folder_img : WindowsPath
        WindowsPath object containing the filepath to the folder containing
        the images.

    Returns
    -------
    pts_names : list
        A list containing all pointfile names that are present in the folder
        specified by folder_pts.
    img_names : list
        A list containing all image names that are present in the folder
        specified by folder_img.

    """
    # Get image file names from list
    # opening the file in read mode
    my_file = open(imglist, "r")
    # reading the file
    data = my_file.read()
    # Convert to list, where each line in the text document becomes a separate
    # list item
    list_items = data.split("\n")
    
    pts_names = []
    img_names = []
    # Extract the point file names and image file names from the imagelist
    # The first 8 line and last line of the document are skipped since these
    # don't contain any file data.
    for item in list_items[10:-1]:
        files = item.split(" : ")
        
        path_pts = folder_pts / files[0]
        path_img = folder_img / files[1]
        
        # Check if both files exists, add names to lists, otherwise print 
        # missing file info
        if path_pts.exists() == True and path_img.exists() == True:
            pts_names.append(files[0])
            img_names.append(files[1])
        elif path_pts.exists() == False:
            print('Points file does not exists for', files[0])
        else: print('Image file does not exists for', files[1])
        
    return pts_names, img_names


def load_full_body_points(img, folder_pts):
    """
    Loads both _L and _R points files from filepath indicated by folder. 
    Files are only loaded if both L and R points file exist for the patient.
    Points files are presumed to be in '*.pts' format.
    Please note that due to the naming convention of Bonefinder, the _L points
    belong to the RIGHT hip and the _R points belong to the LEFT hip.
    
    Parameters
    ----------
    img : str
        Name of the image for which the point files should be loaded.
    folder_pts : Windowspath
        Windowspath to folder containing points files.
        
    Returns
    -------
    pts_data_L : list
        List containing left point data (numpy array) for the patient (RIGHT hip).
    pts_data_R : list
        List containing right point data (numpy array) for the patient (LEFT hip).
    """
   
    pts_L = img + ('_L.pts')
    pts_R = img + ('_R.pts')
    
    path_pts_L = folder_pts / pts_L
    path_pts_R = folder_pts / pts_R
    
    # If both point files exist, load data, otherwise print missing file info
    if path_pts_L.exists() == True and path_pts_R.exists() == True:
        pts_data_L = load_point_data(path_pts_L)
        pts_data_R = load_point_data(path_pts_R)
    elif path_pts_L.exists() == False:
        pts_data_L = []
        pts_data_R = []
        print('Left points file does not exists for', pts_L)
    else: 
        pts_data_L = []
        pts_data_R = []
        print('Right points file does not exists for', pts_R)   
        
    return pts_data_L, pts_data_R

