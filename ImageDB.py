"""
This file will create the image database. It will first see if the database exist, if it does it will use one of the
files and the anlyzation to help create the photomosaic. For analyzing the photo we will simply keep the images in a
20 by 20 size and get the average in four quadrants.
"""

from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib import request
import cv2
import heapq
import numpy as np
import glob, os
import json
#global
pixel_size = 20


def average_color(src):
    """
    This will get the average color of the image. It will return a tuple of the average color which will be used for the
    photomosaic. It will at least need the source. The other values are used with our based image.

    :param src:
    :return average_color_tuple:
    """

    r, g, b = 0, 0, 0
    count = 0
    for x in range(pixel_size):
        for y in range(pixel_size):
            tempR, tempG, tempB = src[x, y]
            r += tempR
            g += tempG
            b += tempB
            count += 1

    # calculate averages
    average_color_tuple = ((r/count), (g/count), (b/count))
    return average_color_tuple


def db_image_resize(img_url):
    """
    This method will change the size of the image. This is used for the max_color and stitching. This is going to be
    for an 20 by 20 image.
    :param img_url:
    :return newsize_img:
    """
    # save the image temporary to do the processing
    request.urlretrieve(img_url, "temp.jpg")

    img = cv2.imread("temp.jpg")
    newsize_img = cv2.resize(img, (pixel_size, pixel_size))
    return newsize_img


def image_db_scrapper(src, filename):
    """
    This file is going to create your DB aka dictionary of images with urls, max color, and number of used set to 0
    This is done by taking your source given and scrapping all the images urls using BEAUTIFULSOUP4

    Showing processing for more info to the user. Instead of wondering if it is working
    :param src:
    :param filename:
    :return images:
    """

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

    while count <= 200:
        print("Process 2k Images! Percentage Complete: " + "{0:.0f}%".format((count/2000)*100))

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
                newsize_img = db_image_resize(img_src)
                # newsize_img = cv2.imread(newsize_img)
                color = average_color(newsize_img)
                used_count = 0
                # images[img.get('src')] = [color]
                images[img_src] = [color]


        # We got all the photos now we will change the url by one
        src2 = src2.replace("-st" + str(increase_page) + "00", "-st" + str(increase_page+1) + "00")
        increase_page += 1
        # Now we will reload the html object
        html_page = urllib2.urlopen(src2)

    file = open(os.path.join("./image_db", filename +".txt"), 'w')
    # for i in images:
    #     file.write('%s:%s\n' % (i, images[i]))
    file.write(json.dumps(images))
    file.close()

    return images

