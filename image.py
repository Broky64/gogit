import cv2 
import numpy as np
from matplotlib import pyplot as plt

def find_intersections(lines):
    intersections = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            x1, y1, x2, y2 = lines[i]
            x3, y3, x4, y4 = lines[j]
            
            # Calcul des coordonnées de l'intersection
            denominator = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
            
            if denominator != 0:
                ua = (((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))) / denominator
                ub = (((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))) / denominator
                
                # Vérifiez si l'intersection se trouve dans le segment de ligne
                if 0 <= ua <= 1 and 0 <= ub <= 1:
                    x = int(x1 + ua * (x2 - x1))
                    y = int(y1 + ua * (y2 - y1))
                    intersections.append((x, y))
    return intersections

# Fonction pour afficher les lignes et les intersections
def display_lines(img, lines, intersections):
    for line in lines:
        x1, y1, x2, y2 = line
        cv2.line(img, (x1, y1), (x2, y2),(0, 255, 0), 2)
        cv2.circle(img, (x1, y1), 1, (255, 0, 0), 2)
        cv2.circle(img, (x2, y2), 1, (255, 0, 0), 2)
    for intersection in intersections:
        cv2.circle(img, intersection, 3, (0, 0, 255), -1)
    cv2.imshow('image avec les lignes et les intersections', img)
    cv2.waitKey(0)

# Lire l'image et détecter les bords
img = cv2.imread('coup1.png', cv2.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv2.Canny(img, 100, 200)

# Détecter les lignes dans les contours
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=80, maxLineGap=20)
lines = np.squeeze(lines)

# Trouver les intersections des lignes détectées
intersections = find_intersections(lines)
print("Nombre d'intersections détectées:", len(intersections))

# Afficher les lignes et les intersections sur l'image
display_lines(img, lines, intersections)
