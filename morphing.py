import cv2
import numpy as np

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

from matplotlib import pyplot as plt

img1 = cv2.imread('hillary_clinton.jpg') # query image

gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 100,0.01,10)
corners = np.float32(corners)
print(corners)
for i in corners:
    x,y = i.ravel()
    cv2.circle(img1,(x,y),3,255,-1)


plt.imshow(img1),plt.show()

