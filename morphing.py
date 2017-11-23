import cv2
from json import *
import numpy as np
import os
#import requests
import json
import random

########## merging
# img1 = cv2.imread("base.jpg")
# img2 = cv2.imread("hillary_clinton.jpg")
#
# newsize_img = cv2.resize(img1, (500, 500))
# cv2.imwrite("base.jpg", newsize_img)
#
# newsize_img = cv2.resize(img2, (500, 500))
# cv2.imwrite("hillary_clinton.jpg", newsize_img)
#
# img1 = cv2.imread("base.jpg")
# img2 = cv2.imread("hillary_clinton.jpg")
#
# dst = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
# cv2.imshow('dst', dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# This is used temp for a quick resize of all images. One time use. Then I removed all jpg.
def resize_presidents():
    for filename in os.listdir("./based_image_db"):
        if filename.endswith(".jpg"):
            img1 = cv2.imread("./based_image_db/" + filename)
            newsize_img = cv2.resize(img1, (500, 500))
            cv2.imwrite("./based_image_db/" + filename[:-4] + ".png", newsize_img)
            os.remove("./based_image_db/" + filename)


### We are going to try and use an api to get the cordinates of what we need :S
def get_facial_landscapes():
    for filename in os.listdir("./based_image_db"):
        if filename.endswith(".png"):
            print("New Image!!!!!!"+filename+"\n\n")
            url = "https://api-us.faceplusplus.com/facepp/v3/detect"
            data={"api_key":"Nvs5_JbdDW6WsYKVCeGXy6e8S4USNxim",
                  "api_secret":"sEsX4zUtz2ZizNLA_GLZqvhGyWMl364Q",
                  "return_landmark":1}
            files={
                "image_file":open("./based_image_db/" + filename,"rb")
            }
            response = requests.post(url, data=data, files=files)
            req_con=response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            # python reads the entire json as dictionaries so we call each key until value of x and y
            # IDE terminal may cause issues try in commandline
            f = open("./facial_landscapes/" + filename[:-4]+".txt",'w')

            for i in req_dict["faces"][0]["landmark"]:
                f.write(str(req_dict["faces"][0]["landmark"][i]["x"]) + " "
                        + str(req_dict["faces"][0]["landmark"][i]["y"]) + "\n")
                print(req_dict["faces"][0]["landmark"][i]["x"])
                print(req_dict["faces"][0]["landmark"][i]["y"])
                print()
            f.close()






# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color ) :

    triangleList = subdiv.getTriangleList()
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
        cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
        cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)


if __name__ == '__main__':

    # Define window names
    win_delaunay = "Delaunay Triangulation"

    # Define colors for drawing.
    delaunay_color = (255,255,255)

    # Read in the image.
    img = cv2.imread("./based_image_db/43.png")

    # Keep a copy around
    img_orig = img.copy()

    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])

    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect)

    # Create an array of points.
    points = []

    # Read in the points from a text file
    with open("./facial_landscapes/43.txt") as file:
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))

    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)

    # Draw delaunay triangles
    draw_delaunay( img, subdiv, (255, 255, 255) )



    # Show results
    cv2.imshow(win_delaunay,img)
    cv2.waitKey(0)


