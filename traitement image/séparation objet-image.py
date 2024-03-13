import numpy as np
import cv2 as cv
from scipy.spatial.distance import cdist


# Charger l'image
image = cv.imread('plateau_pied.jpg')
image = cv.resize(image, (800, 800))
img=image.copy()


# Convertir l'image en niveaux de gris
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Appliquer un seuillage adaptatif
thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)

# Appliquer une détection de contours
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dessiner les contours détectés sur une image vide
contour_img = np.zeros_like(img)
cv.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
biggest = np.array([])
max_area=0
for i in contours:
    area = cv.contourArea(i)
    if area > 50:
        peri = cv.arcLength(i, True)
        approx = cv.approxPolyDP(i, 0.03 * peri, True)
        if area > max_area :
            biggest = approx
            max_area = area
            M = cv.moments(i)
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

cv.circle(contour_img, (center_x, center_y), 25, (255, 0, 255), -1)

points_proches = []
etat=False
biggest = biggest.reshape(-1, 2)
print('biggest',biggest[0])
list_indice=[]
for i in range (len(biggest)):
    if i not in list_indice:
        List_médian=[]
        x1 ,y1 = biggest[i]
        List_médian.append([x1, y1])
        for j in range(i+1,len(biggest)):
            x2 ,y2 = biggest[j]
            distance = ((x2-x1)**2+(y2-y1)**2)**(1/2)
            if distance < 50:
                list_indice.append(j)
                List_médian.append([x2,y2])
        points_proches.append(List_médian)
print('points_proches',points_proches)
points_correctes = []
for i in range(len(points_proches)):
    min_distance = float('inf')  # Réinitialisation de la distance minimale pour chaque sous-liste de points
    if len(points_proches[i]) > 1:
        indice=0
        for j in range(len(points_proches[i])):
            point = points_proches[i][j]
            x0, y0 = point
            distance = ((center_x - x0) ** 2 + (center_y - y0) ** 2) ** (1 / 2)
            if distance < min_distance or j == 0:
                min_distance = distance
                indice = j
        points_correctes.append(points_proches[i][indice])
    else:
        points_correctes.append(points_proches[i][0])
print(points_correctes)
points_correctes=points_correctes[1:]


points_correctes = np.array(points_correctes)
print(points_correctes)
points_correctes = points_correctes.reshape((4, 2))
points_ordre = np.zeros((4, 1, 2), dtype=np.int32)

add = points_correctes.sum(axis=1)
min_index = np.argmin(add)
max_index = np.argmax(add)
points_ordre[0] = points_correctes[min_index-1]
points_ordre[3] = points_correctes[max_index-1]

diff = np.diff(points_correctes, axis=0)  # Modification ici, axis=0
min_index = np.argmin(diff)
max_index = np.argmax(diff)
points_ordre[1] = points_correctes[min_index-1]
points_ordre[2] = points_correctes[max_index-1]
print(points_ordre)



x1, y1 = points_ordre[0][0]
x2, y2 = points_ordre[1][0]
x3, y3 = points_ordre[2][0]
x4, y4 = points_ordre[3][0]
print(x1,y1)
#for elem in points_correctes:
#    x, y = elem
cv.circle(contour_img, (x3, y3), 5, (0, 0, 255), -1)

pts_source = np.array([[x2, y2], [x3, y3], [x4, y4], [x1, y1]], dtype=np.float32)

# Définir les nouvelles positions des coins après la transformation
# Par exemple, pour une sortie de taille fixe, vous pouvez utiliser :
width = 800  # Largeur de l'image de sortie
height = 800  # Hauteur de l'image de sortie
pts_destination = np.array([[0, 0], [width, 0], [0, height], [width, height]], dtype=np.float32)

# Calculer la matrice de transformation de perspective
matrix = cv.getPerspectiveTransform(pts_source, pts_destination)

# Appliquer la transformation de perspective à l'image d'origine
new_image = cv.warpPerspective(image, matrix, (width, height),flags=cv.INTER_LINEAR)

    # Afficher l'image avec les contours détectés
#cv.imshow('Detected Contours', contour_img)
cv.imshow('Detected Contours', new_image)
cv.waitKey(0)
cv.destroyAllWindows()