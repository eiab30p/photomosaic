#!/usr/bin/env python
"""
Description:
The project is making a photometric. This means taking one photo and making it with thousands of smaller
photos based on color in that area. We are doing this by first collecting the photos urls and getting the most
prominent color in that photo as a whole (????) then we will store it into a dictionary (image url, color, and used#)
once that is completed I will iterate over the based image 8 pixels at a time and then find the image that matches
the color in the base and then start sticking the photos together.

Additional Tools:
    BeautifulSoup4
        $ pip install beautifulsoup4
    OpenCV
        $ pip install opencv

Running:
    $ python photomosaics.py

TODO:
Find the photo DB without water marks but also allow web crawling
Do a better URL validation

Honor Code:
On my honor, I have not given, nor received, nor witnessed any unauthorized assistance on this work.
    I worked on this assignment alone, using only this semester's course materials.

Other Sources:
 https://docs.python.org/2/library/heapq.html
 https://stackoverflow.com/questions/3019909/using-an-index-to-get-an-item-python
 https://pypi.python.org/pypi/python-resize-image
 https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
 https://stackoverflow.com/questions/33689705/how-to-compare-values-in-tuples-in-a-list


@author: Eduardo "Eddy" Verde & David Maldonado
@author email: everde@rollins.edu & dmalsonado@rollins.edu
"""

from __future__ import print_function
from random import randint
from PIL import Image
from ImageDB import *
import cv2
import math

pixel_size = 20
blank_image_size = 1000

def get_random_image(base_avg, db_images):
    """

    :param base_avg:
    :param db_images:
    :return:
    """
    list_of_possible_urls = []
    for k in db_images:
        results = math.sqrt(
            (db_images[k][0][0] - base_avg[0])**2 +
            (db_images[k][0][1] - base_avg[1])**2 +
            (db_images[k][0][2] - base_avg[2])**2
        )
        if results < 100:
            list_of_possible_urls.append(k)

    img_url = list_of_possible_urls[randint(0, len(list_of_possible_urls) - 1)]
    return img_url


def base_image_processing(mosaic_in, db_images):
    """

    :param mosaic_in:
    :param db_images:
    :return:
    """

    blank_photomosaic_image = Image.new("RGB", (blank_image_size, blank_image_size))

    # determine the size of the mosaic image
    rows, cols = mosaic_in.shape[:2]

    # loop through the image
    for i in range(0, rows, pixel_size):
        for j in range(0, cols, pixel_size):
            avg_color = average_color(i, i + pixel_size, j, j + pixel_size, mosaic_in)
            tile_url = get_random_image(avg_color, db_images)
            db_image_resize(tile_url)
            tile_image = Image.open("temp.jpg")
            blank_photomosaic_image.paste(tile_image, (i, j))
        print("Creating Image Please Wait....." + "{0:.0f}%".format((i/blank_image_size)*100))
    blank_photomosaic_image.save("photomosaic.jpg")
    sideways_image = Image.open("photomosaic.jpg")
    corrected_image = sideways_image.rotate(270)
    corrected_image.save("photomosaic.jpg")


if __name__ == '__main__':
    """
    
    """
    # Introduction, this is what you need to do and what page to search.
    print("Welcome to Photomosaic Application!\n"
          "Before we proceed on please make sure you have a photo\n"
          "save in the same directory as this file and name it 'base.jpg'.\n"
          "Once that is complete make sure you are using the following\n"
          "website for the images. If you do not have a site a default one will\n"
          "be used. Good Luck and Have Fun!\n\n"
          "Website for Images: https://depositphotos.com/\n"
          "Example: https://depositphotos.com/search/space.html\n"
          "Type \"None\" if you want default else enter url:")

    # Getting user input and validating it. If there are an error we will default to a traveling image database.
    src = input()
    if src.upper() == "NONE":
        src = "https://depositphotos.com/search/traveling.html"
    if len(src) <= 23:
        print("URL is invalid, using default")
        src = "https://depositphotos.com/search/traveling.html"

    # This is checking if the database is already created in the photomosaic.image_db directory to reduce the time of collecting
    # images each time. You need to have at least one in the directory to work

    print("Checking if Database already exist.")
    search_file_name = src[33:-5]
    db_exist = False
    for file in os.listdir("./photomosaic.image_db"):
        if file == (search_file_name + ".txt"):
            print("Database Exist, Let's Create a Mosaic")
            db_exist = True

    if not db_exist:
        print("Getting Started with the Processing")
        images = image_db_scrapper(src, search_file_name)
        print("Processing Complete! Let's Make a Mosaic!")

    base = cv2.imread("base.jpg")
    base = cv2.resize(base, (blank_image_size, blank_image_size))
    cv2.imwrite("base.jpg", base)
    base = cv2.imread("base.jpg")

    # We are reading the images from text file.
    db_images = json.load(open("./photomosaic.image_db/" + search_file_name + ".txt"))
    base_image_processing(base, db_images)


    # POSSIBILE TODOS
    # TODO: Have the user input photo size and tile size
    # TODO: Have the images rotate around a square to then put into an image.
    # TODO: Morphing two photomosaic
    # TODO: Different Shape images?
