import numpy as np
import cv2 as cv

img = cv.imread("3plateau.jpg")
img = cv.resize(img, (1000, 1000))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray, 5)
circles = cv.HoughCircles(
    gray,
    cv.HOUGH_GRADIENT,
    dp=1.2,
    minDist=20,
    param1=20,
    param2=20,
    minRadius=5,
    maxRadius=15
)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

cv.imshow('detected circles', img)
cv.waitKey(0)
cv.destroyAllWindows()
