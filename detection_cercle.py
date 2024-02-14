import cv2
import numpy as np
import imutils

# Load an image
img = cv2.imread('coup1.png')

# Resize the image if its width is greater than 600 pixels
if img.shape[1] > 600:
    img = imutils.resize(img, width=600)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image
ret, gray_threshed = cv2.threshold(gray, 8, 255, cv2.THRESH_BINARY)

# Blur the thresholded image
bilateral_filtered_image = cv2.bilateralFilter(gray_threshed, 5, 175, 175)

# Detect edges using Canny edge detector
edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_list = []
for contour in contours:
    # Approximate contours to polygons and check if it's a circle
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    area = cv2.contourArea(contour)
    if len(approx) > 8 and area > 10:
        contour_list.append(contour)


# Draw contours on the original image
clone = img.copy()
cv2.drawContours(clone, contour_list, -1, (255, 0, 0), 2)

# Print the number of circles detected
print('Number of found circles: {}'.format(int(len(contour_list))))

# Display the result
cv2.imshow('Objects Detected', clone)
cv2.waitKey(0)
cv2.destroyAllWindows()