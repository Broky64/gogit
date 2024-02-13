import cv2
import numpy as np

# Charger l'img et la redimensionner
img = cv2.imread('coup1.png')
img = cv2.resize(img, (500, 500))

# Convertir l'img en niveaux de gris
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Binarisation de l'img
gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

# Détection des lignes
lines = cv2.HoughLinesP(gray, 1, np.pi/180, 80, minLineLength=80, maxLineGap=20)  # Ajustement des paramètres

# Extension des lignes jusqu'aux bords de l'img
height, width = img.shape[:2]
extended_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]

    # Calcul de la pente
    if x2 - x1 != 0:  # Vérifier si le dénominateur n'est pas nul
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf')  # Gérer le cas de la pente infinie (ligne verticale)

    # Calcul de l'intersection avec le bord de l'img
    if x1 == x2:
        new_x1, new_y1, new_x2, new_y2 = x1, 0, x1, height
    elif slope == 0:
        new_x1, new_y1, new_x2, new_y2 = 0, y1, width, y1
    else:
        intercept = y1 - slope * x1  # Calcul de l'intercept
        new_y1 = 0
        new_x1 = int((new_y1 - intercept) / slope)
        new_y2 = height
        new_x2 = int((new_y2 - intercept) / slope)

    extended_lines.append([[new_x1, new_y1, new_x2, new_y2]])

# Détection des intersections entre les lignes
intersections = []
for i in range(len(extended_lines)):
    for j in range(i+1, len(extended_lines)):
        line1 = extended_lines[i][0]
        line2 = extended_lines[j][0]

        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        # Calcul des coordonnées de l'intersection
        denominator = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
        if denominator != 0:
            ua = (((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))) / denominator
            ub = (((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))) / denominator

            # Vérification si les lignes se croisent
            if 0 <= ua <= 1 and 0 <= ub <= 1:
                intersection_x = int(x1 + (ua * (x2 - x1)))
                intersection_y = int(y1 + (ua * (y2 - y1)))
                intersections.append((intersection_x, intersection_y))

# Dessiner les intersections
for point in intersections:
    cv2.circle(img, point, 5, (255, 0, 0), -1)

# Compter le nombre d'intersections
num_intersections = len(intersections)
print("Nombre d'intersections détectées :", num_intersections)

# Affichage de l'img
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
