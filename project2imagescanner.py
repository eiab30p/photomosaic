# Project 2: True Photomosaic
#
# Collaboration Statement here: 
#
# David Maldonado & Roberto Vargas
#links to resources used:
#https://stackoverflow.com/questions/3019909/using-an-index-to-get-an-item-python
#https://pypi.python.org/pypi/python-resize-image
#https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
#https://stackoverflow.com/questions/33689705/how-to-compare-values-in-tuples-in-a-list
#image database: https://github.com/caesar0301/awesome-public-datasets#image-processing

import numpy as np
import cv2
import glob
import os

#determine the path where the images are located
file_path = "C:\\Users\\Nzxt\\Desktop\\project2\\dog"
#loop through each file that matches the parameters
for infile in glob.glob( os.path.join(file_path, '*.jpg*') ):
    #read in each file
    image = cv2.imread(infile)
    # get image as numpy array
    image = np.array(image)
    # get shape
    rows,cols, colors = image.shape
    image.shape = (rows*cols, colors)
    #write the bgr mean to a file, along with the file name and a new line
    with open("C:\\Users\\Nzxt\\Desktop\\project2\\image_tuples.txt", "a") as f:
        f.write(str(tuple(np.mean(image, axis = 0)))+ "\n")
        
file_path = "C:\\Users\\Nzxt\\Desktop\\project2\\dog"
#loop through each file that matches the parameters
for infile in glob.glob( os.path.join(file_path, '*.jpg*') ):
    #read in each file
    image = cv2.imread(infile)
    # get image as numpy array
    image = np.array(image)
    # get shape
    rows,cols, colors = image.shape
    image.shape = (rows*cols, colors)
    #write the bgr mean to a file, along with the file name and a new line
    with open("C:\\Users\\Nzxt\\Desktop\\project2\\image_names.txt", "a") as f:
        f.write(infile + "\n")



    