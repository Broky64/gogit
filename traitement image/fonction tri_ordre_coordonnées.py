import itertools
import numpy as np
import cv2 as cv
from scipy.spatial.distance import cdist
import math

def calculer_aire(point1, point2, point3, point4):
    # Convertir les points en tableaux numpy pour une manipulation plus aisée
    p1, p2, p3, p4 = np.array(point1), np.array(point2), np.array(point3), np.array(point4)
    
    # Calculer les vecteurs diagonaux du quadrilatère
    diag1 = p2 - p4
    diag2 = p1 - p3
    
    # Calculer les produits croisés des vecteurs diagonaux
    produit_croise = np.cross(diag1, diag2)
    
    # Calculer l'aire du quadrilatère
    aire = 0.5 * np.abs(produit_croise)
    
    return aire

def proche_aire(aire1, aire2):
    return abs(aire1 - aire2)

def points_correctes(biggest, aire_cherchée):
    aire=0
    diff = proche_aire(aire,aire_cherchée)
    indice=[]
    'distance_centre=[]
    'index_coins= []
    for elem in points_correctes:
        x, y = elem
        distance = ((center_x - x) ** 2 + (center_y - y) ** 2) ** (1 / 2)
        distance_centre.append(distance)
    for i in range (len(distance_centre)):
        eq_dist = [distance_centre[i]]
        index_coins=[i]
        for j in range (i+1,len(distance_centre)):
            if abs(distance_centre[i]-distance_centre[j])<50:
                eq_dist.append(distance_centre[j])
                index_coins.append(j)
            if len(eq_dist) ==4:
                for index in index_coins:
                    bons_coins.append(points_correctes[index])'
    for indice1 in range(len(biggest)):
        for indice2 in range(len(biggest)):
            if indice2!=indice1:
                for indice3 in range(len(biggest)):
                    if indice3!= indice1 and indice3!= indice2:
                        for indice4 in range(len(biggest)):
                            if indice4!= indice1 and indice4!= indice2 and indice4!=indice3:
                                point1 = biggest[indice1]
                                point2 = biggest[indice2]
                                point3 = biggest[indice3]
                                point4 = biggest[indice4]
                                aire1=calculer_aire(point1, point2, point3, point4)
                                diff1 = proche_aire(aire1,aire_cherchée)
                                if diff1<diff:
                                    diff = diff
                                    aire = aire1
                                    indice=[indice1,indice2,indice3,indice4]
    return(indice)



# Charger l'image
image = cv.imread('plateau_pied3.jpg')
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
print('biggest',biggest, 'area',max)
indice = points_correctes(biggest, max_area)
bons_coins=[biggest[indice[0]],biggest[indice[1]],biggest[indice[2]],biggest[indice[3]]]
bons_coins = list(bons_coins)
        

print('bons_coins',bons_coins)
bons_coins = sorted(bons_coins, key=lambda coord:coord[0])
bons_coins[:2] = sorted(bons_coins[:2],key=lambda coord:coord[1])
bons_coins[2:] = sorted(bons_coins[2:],key=lambda coord:coord[1])


points_ordre = bons_coins

x1, y1 = points_ordre[0]
x2, y2 = points_ordre[1]
x3, y3 = points_ordre[2]
x4, y4 = points_ordre[3]
print('points_ordre', points_ordre)
cv.circle(contour_img, (x4, y4), 15, (0, 0, 255), -1)

pts_source = np.array([[x2, y2], [x1, y1], [x4, y4], [x3, y3]], dtype=np.float32)

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
cv.imshow('Detected Contours', contour_img)
#cv.imshow('Detected Contours', new_image)
cv.waitKey(0)
cv.destroyAllWindows()


# Exemple d'utilisation
#liste_points = [( 96, 237), (429, 257), (149, 609), (680, 615), (668, 279), (684, 619), (145, 613), (180, 259), (418, 628),(127, 632), (698, 632),(418, 628), (647, 251)]
#liste_points = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2)]
#aire_voulue = 184070.5
#aire_voulue=1.5
#resultat = trouver_quadrilatere_proche(liste_points, aire_voulue)
#print("Les points du quadrilatère avec l'aire la plus proche de", aire_voulue, "sont :", resultat)

