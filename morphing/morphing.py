#!/usr/bin/env python

import numpy as np
import cv2
import sys

# Read points from text file
def readPoints(path):
    # Create an array of points.
    points = []
    tri = []
    # Read points
    count = 0
    with open(path) as file :
        for line in file:
            if count % 4 == 0 and count != 0:
                points.append((tri[0], tri[1], tri[2]))
                tri = []
            else:
                x, y = line.split()
                tri.append((int(x), int(y)))
            count = count + 1
    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []

    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]), (t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    print(r)
    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask


if __name__ == '__main__' :

    filename1 = './morphing.based_image_db/normalJason.png'
    filename2 = './morphing.based_image_db/aquaJason.png'
    alpha = 0.4

    # Read images
    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)

    # Convert Mat to float data type
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    tri1 = './triangulation_points/start.txt'
    tri2 = './triangulation_points/end.txt'
    tri3 = './triangulation_points/0.4.txt'

    # Read array of corresponding points
    points1 = readPoints(tri1)
    points2 = readPoints(tri2)
    points = readPoints(tri3)


    # Allocate space for final output
    imgMorph = np.zeros(img1.shape, dtype=img1.dtype)

    for i in range(len(points1)):
        t1 = [points2[i][0], points2[i][1], points2[i][2]]
        t2 = [points2[i][0], points2[i][1], points2[i][2]]
        t = [points1[i][0], points1[i][1], points1[i][2]]

        # Morph one triangle at a time. (imag1,imag2, blank morphing, triangle1,2,3, and alpha
        morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)


    # Display Result
    cv2.imshow("Morphed Face", np.uint8(imgMorph))
    cv2.waitKey(0)
