import numpy as np
import cv2 as cv
from scipy.spatial.distance import cdist


# Charger l'image
img = cv.imread('plateau_pied.jpg')
img = cv.resize(img, (800, 800))

# Convertir l'image en niveaux de gris
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Appliquer un seuillage adaptatif
thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)

# Appliquer une détection de contours
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dessiner les contours détectés sur une image vide
contour_img = np.zeros_like(img)
cv.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
max_contour = max(contours, key=cv.contourArea)

# Calculer le centre du contour maximal
M = cv.moments(max_contour)
center_x = int(M["m10"] / M["m00"])
center_y = int(M["m01"] / M["m00"])

# Initialiser les variables pour le contour avec la plus grande aire et son aire maximale
biggest = None
max_area = 0

# Parcourir tous les contours
for contour in contours:
    area = cv.contourArea(contour)
    if area > max_area:
        biggest = contour
        max_area = area

# Extraire les coordonnées des points du contour maximal
contour_points = max_contour.reshape(-1, 2)

# Calculer la distance entre chaque paire de points
distances = cdist(contour_points, contour_points)

# Créer une liste pour stocker les groupes de points
grouped_points = []

# Parcourir les distances et regrouper les points qui ont une distance de moins de 50 pixels
for i in range(len(contour_points)):
    group = [j for j in range(len(contour_points)) if distances[i, j] < 50]
    if group not in grouped_points:
        grouped_points.append(group)
print(grouped_points)

# Afficher l'image avec le quadrilatère de plus petite aire
cv.imshow('Min Area Quadrilateral', contour_img)
cv.waitKey(0)
cv.destroyAllWindows()







