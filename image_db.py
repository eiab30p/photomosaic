"""
This is file will create an image database based on prior and new images from a URL
The images will be stored in a file based on the searched name.
"""

from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib import request
import cv2
import heapq
import numpy as np

#global
pixel_size = 15


def max_color(src, row = 0, col=0, size=pixel_size, max_row = 0, max_col = 0):
    """
    This will get the 3 top colors for a picture to use in your photomosaic. It will at least need the source.
    The other values are used with our based image. This is how we are going to get the max color of our base image
    section and the smaller image maxes  to be able to stich them together.
    This method was mostly used from the pixelizer image

    :param src:
    :param row:
    :param col:
    :param size:
    :return top_three_max:
    """
    pixel_map = []
    color = {}
    if (col + pixel_size) > src.shape[0]:
        endingcol = src.shape[0] - 1
    else:
        endingcol = col + pixel_size

    if (row + pixel_size) > src.shape[1]:
        endingrow = src.shape[1] - 1
    else:
        endingrow = row + pixel_size
    try:
        # This is where the Fun is. We are looping within a calculated space to find the common colors.
        # print(src.shape)
        # print(col+pixel_size, row + pixel_size)


        # print(endingcol, endingrow)

        for newY in range(col, endingcol):
            for newX in range(row, endingrow):
                # We are now adding the tuple of the pixels into the pixel map.
                pixel_map.append((newY, newX))
                # We are now getting the RGB tuple as our key
                # print(newY, newX)
                # print(newY,newX)
                rbg = (src[newY][newX][0], src[newY][newX][1] , src[newY][newX][2] )
                # we are taking the RGB tuple to see if it is a key well add one it our value if not create the key
                if rbg in color:
                    color[rbg] += 1
                else:
                    color[rbg] = 1

        # trying to get the top three max for multiple so I decided to see if a heap would be faster. It seems to be true
        # https://docs.python.org/2/library/heapq.html
        top_three_max = heapq.nlargest(3, color, key=color.get)
        return top_three_max
    except :
        return top_three_max


def db_image_resize(img_url):
    """
    This method will change the size of the image. This is used for the max_color and stitching. This is going to be
    for an 8 by 8 image.
    :param img_url:
    :return newsize_img:
    """
    # save the image temporary to do the processing
    request.urlretrieve(img_url, "temp.jpg")

    img = cv2.imread("temp.jpg")
    newsize_img = cv2.resize(img, (pixel_size, pixel_size))
    return newsize_img


def image_db(src):
    """
    This file is going to create your DB aka dictionary of images with urls, max color, and number of used set to 0
    This is done by taking your source given and scrapping all the images urls using BEAUTIFULSOUP4

    Showing processing for more info to the user. Instead of wondering if it is working
    :param src:
    :return images:
    """

    # src = "https://depositphotos.com/search/space.html"
    # Getting the web page object based off the url
    html_page = urllib2.urlopen(src)

    # adding the "-st100.html" because moving from page to page I noticed that
    # the ending of the url changes only so I added the ending so I can use it for
    # processing later.
    src2 = src[:-5]+"-st100.html"

    # count is the number of images collected. Currently it is 9k
    # increase_page is to change the url
    count = 1
    increase_page = 0
    images = {}

    while count <= 2000:
        print("Process 1k Images! Percentage Complete: " + "{0:.0f}%".format((count/2000)*100))

        # Issue while using BeautifulSoup needed parser the solution was found in the below link
        # https://stackoverflow.com/questions/36192122/beautifulsoup-html-parser-error
        soup = BeautifulSoup(html_page, 'html.parser')

        # While at the page of the url loop through and get all the img tags shown.
        for img in soup.findAll('img'):
            count += 1
            # print(img.get('src'))
            img_src = img.get('src')
            # removing icons in the image that are collected
            if img_src[1] == '/':
                pass
            else:
                newsize_img = db_image_resize(img.get('src'))
                # newsize_img = cv2.imread(newsize_img)
                color = max_color(newsize_img)
                used_count = 0
                # images[img.get('src')] = [color]
                images[color[0]] = [img.get('src')]
                images[color[1]] = [img.get('src')]
                images[color[2]] = [img.get('src')]



        # We got all the photos now we will change the url by one
        src2 = src2.replace("-st" + str(increase_page) + "00", "-st" + str(increase_page+1) + "00")
        increase_page += 1
        # Now we will reload the html object
        html_page = urllib2.urlopen(src2)

    return images

