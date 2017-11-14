"""
This file will create the image database. It will first see if the database exist, if it does it will use one of the
files and the anlyzation to help create the photomosaic. For analyzing the photo we will simply keep the images in a
20 by 20 size and get the average in four quadrants.
"""

from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib import request
import cv2
import os
import json

# global
from MainPhotomosaic import pixel_size


def average_color(row_start, row_stop, col_start, col_stop, src):
    r, g, b, count = 0, 0, 0, 0
    for row in range(row_start, row_stop):
        for col in range(col_start, col_stop):
            r += src[row, col][0]
            b += src[row, col][1]
            g += src[row, col][2]
            count += 1

    # Return image that first this average
    return float(r) / float(count), float(g) / float(count), float(b) / float(count)


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
    cv2.imwrite("temp.jpg", newsize_img)
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

    while count <= 5000:
        print("Process 2k Images! Percentage Complete: " + "{0:.0f}%".format((count/5000)*100))

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
                color = average_color(0, pixel_size, 0, pixel_size, newsize_img)
                images[img_src] = [color]

        # We got all the photos now we will change the url by one
        src2 = src2.replace("-st" + str(increase_page) + "00", "-st" + str(increase_page+1) + "00")
        increase_page += 1
        # Now we will reload the html object
        html_page = urllib2.urlopen(src2)

    file = open(os.path.join("./image_db", filename + ".txt"), 'w')
    file.write(json.dumps(images))
    file.close()

    return images
