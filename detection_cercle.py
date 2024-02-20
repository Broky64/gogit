import cv2
import numpy as np

img = cv2.imread('4.jpg')
output = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=60)

if circles is not None:
    detected_circles = np.uint16(np.around(circles))
    centers_list = []  # Liste pour stocker les coordonnées des centres des cercles détectés
    for (x, y, r) in detected_circles[0, :]:
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        cv2.circle(output, (x, y), r, (0, 255, 0), 3)
        centers_list.append((x, y))  # Ajoute les coordonnées du centre à la liste
    print("Coordonnées des centres des cercles détectés:", centers_list)

output = cv2.resize(output, (700, 700))
cv2.imshow('output', output)
cv2.waitKey(0)
