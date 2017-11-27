import cv2
import numpy as np


def gaussian_blur(img):
    return cv2.GaussianBlur(img, (3, 3), 0, 0)


def x_gradient(img):
    return cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3,
                     scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)


def y_gradient(img):
    return cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3,
                     scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def energy(img):
    blurred = gaussian_blur(img)
    gray = grayscale(blurred)
    dx = x_gradient(gray)
    dy = y_gradient(gray)

    return cv2.add(np.absolute(dx), np.absolute(dy))


def cumulative_ener_vertical(energy):
    height, width = energy.shape[:2]
    ener = np.zeros((height, width))

    for i in range(1, height):
        for j in range(width):
            if j - 1 >= 0:
                left = ener[i - 1, j - 1]
            else:
                left = 1e6

            middle = ener[i - 1, j]

            if j + 1 < width:
                right = ener[i - 1, j + 1]
            else:
                right = 1e6

            ener[i, j] = energy[i, j] + min(left, middle, right)

    return ener


def cumulative_ener_horizontal(energy):
    height, width = energy.shape[:2]
    ener = np.zeros((height, width))

    for i in range(1, width):
        for k in range(height):

            if k - 1 >= 0:
                top = ener[k - 1, i - 1]
            else:
                top = 1e6

            middle = ener[k, i - 1]

            if k + 1 < height:
                bottom = ener[k + 1, i - 1]
            else:
                bottom = 1e6

            ener[k, i] = energy[k, i] + min(top, middle, bottom)

    return ener


def horizontal_seam(ener):
    height, width = ener.shape[:2]
    previous = 0
    seam = []

    for i in range(width - 1, -1, -1):
        col = ener[:, i]

        if i == width - 1:
            previous = np.argmin(col)

        else:
            if previous - 1 >= 0:
                top = col[previous - 1]
            else:
                top = 1e6

            middle = col[previous]

            if previous + 1 < height:
                bottom = col[previous + 1]
            else:
                bottom = 1e6

            previous = previous + np.argmin([top, middle, bottom]) - 1

        seam.append([i, previous])

    return seam


def vertical_seam(ener):
    height, width = ener.shape[:2]
    previous = 0
    seam = []

    for i in range(height - 1, -1, -1):
        row = ener[i, :]

        if i == height - 1:
            previous = np.argmin(row)
            seam.append([previous, i])
        else:
            left = row[previous - 1] if previous - 1 >= 0 else 1e6
            middle = row[previous]
            right = row[previous + 1] if previous + 1 < width else 1e6

            previous = previous + np.argmin([left, middle, right]) - 1
            seam.append([previous, i])

    return seam


#### create gif here
def draw_seam(img, seam):
    cv2.polylines(img, np.int32([np.asarray(seam)]), False, (0, 255, 0))
    cv2.imshow('seam', img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def remove_horizontal_seam(img, seam):
    height, width, bands = img.shape
    removed = np.zeros((height - 1, width, bands), np.uint8)

    for x, y in reversed(seam):
        removed[0:y, x] = img[0:y, x]
        removed[y:height - 1, x] = img[y + 1:height, x]

    return removed

def remove_vertical_seam(img, seam):
    height, width, bands = img.shape
    removed = np.zeros((height, width - 1, bands), np.uint8)

    for x, y in reversed(seam):
        removed[y, 0:x] = img[y, 0:x]
        removed[y, x:width - 1] = img[y, x + 1:width]

    return removed


def resize(img, width, height, interactive):
    result = img

    img_height, img_width = img.shape[:2]

    if img_height - height > 0:
        dy = img_height - height
    else:
        dy = 0

    if img_width - width > 0:
        dx = img_width - width
    else:
        dx = 0


    for i in range(dy):
        ener = cumulative_ener_horizontal(energy(result))
        seam = horizontal_seam(ener)
        draw_seam(result, seam)
        result = remove_horizontal_seam(result, seam)

    for i in range(dx):
        ener = cumulative_ener_vertical(energy(result))
        seam = vertical_seam(ener)
        draw_seam(result, seam)
        result = remove_vertical_seam(result, seam)

    # cv2.imwrite('resized.jpg', result)

    print('Press any key to close the window.')

    cv2.imshow('seam', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img = cv2.imread("base.jpg")
    resize(img, width=200, height=200)
