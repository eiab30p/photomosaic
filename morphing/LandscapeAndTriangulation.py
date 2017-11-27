import cv2
from json import *
import numpy as np
import os
#import requests
import json
import random


# This is used temp for a quick resize of all images. One time use. Then I removed all jpg.
def resize_presidents():
    for filename in os.listdir("./morphing.based_image_db"):
        if filename.endswith(".jpg"):
            img1 = cv2.imread("./morphing.based_image_db/" + filename)
            newsize_img = cv2.resize(img1, (500, 500))
            cv2.imwrite("./morphing.based_image_db/" + filename[:-4] + ".png", newsize_img)
            os.remove("./morphing.based_image_db/" + filename)


# We are going to try and use an api to get the cordinates of what we need :S
def get_facial_landscapes():
    for filename in os.listdir("./morphing.based_image_db"):
        if filename.endswith(".png"):
            print("New Image!!!!!!"+filename+"\n\n")
            url = "https://api-us.faceplusplus.com/facepp/v3/detect"
            data={"api_key":"Nvs5_JbdDW6WsYKVCeGXy6e8S4USNxim",
                  "api_secret":"sEsX4zUtz2ZizNLA_GLZqvhGyWMl364Q",
                  "return_landmark":1}
            files={
                "image_file":open("./morphing.based_image_db/" + filename,"rb")
            }
            response = requests.post(url, data=data, files=files)
            req_con=response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            # python reads the entire json as dictionaries so we call each key until value of x and y
            # IDE terminal may cause issues try in commandline
            f = open("./morphing.facial_landscapes/" + filename[:-4]+".txt",'w')

            for i in req_dict["faces"][0]["landmark"]:
                f.write(str(req_dict["faces"][0]["landmark"][i]["x"]) + " "
                        + str(req_dict["faces"][0]["landmark"][i]["y"]) + "\n")

            # Need to add these points to the file for the corners when morphing
            f.write(str(0) + " " + str(0) + "\n")
            f.write(str(0) + " " + str(250) + "\n")
            f.write(str(0) + " " + str(499) + "\n")
            f.write(str(499) + " " + str(0) + "\n")
            f.write(str(499) + " " + str(250) + "\n")
            f.write(str(499) + " " + str(499) + "\n")
            f.write(str(250) + " " + str(0) + "\n")
            f.write(str(250) + " " + str(499) + "\n")
            f.close()


# Visual Image needed?
def morph(img1, img2, alpha):

    dst = cv2.addWeighted(img1, alpha, img2, alpha, 0)
    cv2.imwrite("test_morph.png", dst)
    morph_img = cv2.imread("test_morph.png")
    return morph_img


# Check if a point is inside a rectangle
def rect_contains(rect, point):
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True


def draw_point(img, p, color ):
    cv2.circle( img, p, 2, color, cv2.FILLED, cv2.LINE_AA, 0 )


# Draw delaunay triangles
def delaunay(subdiv):
    triangleList = subdiv.getTriangleList()
    r = (0, 0, 500, 500)
    tri = []
    for t in triangleList:
        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
            tri.append((pt1, pt2, pt3))
    tri.sort(key=lambda pts: (max(pts, key=lambda pt : (pt))))

    return tri


#get weighted points
def weighted_ponts(alpha,pt1, pt2, length_points):
    points = []
    for i in range(0, length_points):
        x = (1 - alpha) * pt1[i][0] + alpha * pt2[i][0]
        y = (1 - alpha) * pt1[i][1] + alpha * pt2[i][1]
        points.append((int(x), int(y)))
    return points


# Read facial landscape points
def readpoints(filename):
    points = []
    with open(filename) as file:
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))
    return points


def create_subdiv(points, rect):
    subdiv = cv2.Subdiv2D(rect)
    for p in points:
        subdiv.insert(p)
    return subdiv


# Write Triangulation to file for morphing
def write_tri_points (tri_points, filename ):
    f = open("./triangulation_points/"+filename+".txt", 'w')

    for i in range(len(tri_points)):
        f.write(str(tri_points[i][0][0]) + " " + str(tri_points[i][0][1]) + "\n")

        f.write(str(tri_points[i][1][0]) + " " + str(tri_points[i][1][1]) + "\n")

        f.write(str(tri_points[i][2][0]) + " " + str(tri_points[i][2][1]) + "\n")

    f.close()


if __name__ == '__main__':

    # Define colors for drawing.
    delaunay_color = (255,255,255)
    points_color = (0, 0, 255)


    # Read in the image.
    start = cv2.imread("./morphing.based_image_db/normalJason.png")
    end = cv2.imread("./morphing.based_image_db/aquaJason.png")

    # Read facial Landscape
    start_txt = "./morphing.facial_landscapes/normalJason.txt"
    end_txt = "./morphing.facial_landscapes/aquaJason.txt"

    # Scope for SubDiv2D
    rect = (0, 0, 500, 500)

    # alpha for weighted points
    alpha = 0.2

    # Create an array of points.
    landscape_points = []
    start_points = []
    end_points = []


    ## Need to do the base and final images first
    start_points = readpoints(start_txt)
    subdiv = create_subdiv(start_points, rect)
    tri_points = []
    tri_points1 = delaunay(subdiv)
    write_tri_points(tri_points1, "start")
    end_points = readpoints(end_txt)
    subdiv = create_subdiv(end_points, rect)
    tri_points = []
    tri_points2 = delaunay(subdiv)
    write_tri_points(tri_points2, "end")






    for i in range(4):
        landscape_points = weighted_ponts(alpha, start_points, end_points, len(start_points))

        #creating scope for delauny
        subdiv = create_subdiv(landscape_points, rect)

        tri_points = []
        tri_points = delaunay(subdiv)

        write_tri_points(tri_points, str(alpha))
        alpha = alpha + .2



