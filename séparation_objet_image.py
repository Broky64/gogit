import numpy as np
import cv2 as cv
from scipy.spatial.distance import cdist

def indices_deux_plus_petites(bons_coins):
    a = bons_coins[0][0]
    b = bons_coins[1][0]
    c = bons_coins[2][0]
    d = bons_coins[3][0]
    # Mettre les valeurs dans une liste avec leurs indices
    valeurs = [(a, 0), (b, 1), (c, 2), (d, 3)]
    # Trier la liste selon les valeurs
    valeurs_triees = sorted(valeurs, key=lambda x: x[0])
    # Renvoyer les indices des deux premières valeurs triées
    return valeurs_triees
def indice_plus_petite(a, b):
    # Mettre les valeurs dans une liste avec leurs indices
    valeurs = [(a, 0), (b, 1)]
    # Trier la liste selon les valeurs
    valeurs_triees = sorted(valeurs, key=lambda x: x[0])
    # Renvoyer les indices des deux premières valeurs triées
    return valeurs_triees



# Charger l'image
image = cv.imread('plateau_pied.jpg')
#image = cv.imread('plateau_pied3.jpg')
image = cv.resize(image, (800, 800))
img1=image.copy()
img2=image.copy()
img3=image.copy()


# Convertir l'image en niveaux de gris
gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

# Appliquer un seuillage adaptatif
thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)

# Appliquer une détection de contours
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Dessiner les contours détectés sur une image vide
contour_img = np.zeros_like(img1)
cv.drawContours(contour_img, contours, -1, (0, 255, 0), 2)


# trouver l'aire la plus grande et les coins de cette aire
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
cv.circle(img2, (center_x, center_y), 15, (255, 0, 255), -1)

for elem in biggest:
    x, y = elem[0]
    cv.circle(img2, (x, y), 15, (0, 0, 255), 1)



points_proches = []
etat=False
biggest = biggest.reshape(-1, 2)
print('biggest',biggest, 'area',max)
list_indice=[]
for i in range (len(biggest)):
    if i not in list_indice:
        List_médian=[]
        x1 ,y1 = biggest[i]
        #cv.circle(contour_img, (x1, y1), 15, (0, 255, 255), -1)
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

distance_centre=[]
index_coins= []
bons_coins=[]
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
            bons_coins.append(points_correctes[index])
for elem in bons_coins:
    x, y = elem
    cv.circle(img3, (x, y), 15, (0, 0, 255), -1)
        

print('bons_coins',bons_coins)
bons_coins = sorted(bons_coins, key=lambda coord:coord[0])
bons_coins[:2] = sorted(bons_coins[:2],key=lambda coord:coord[1])
bons_coins[2:] = sorted(bons_coins[2:],key=lambda coord:coord[1])


points_ordre = bons_coins

x1, y1 = points_ordre[0]
x2, y2 = points_ordre[1]
x3, y3 = points_ordre[2]
x4, y4 = points_ordre[3]
#print('points_ordre', points_ordre)
#cv.circle(contour_img, (x4, y4), 15, (0, 0, 255), -1)

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

# Redimensionner les images pour qu'elles aient la même hauteur
height = min(image.shape[0], contour_img.shape[0], img2.shape[0], img3.shape[0])
image = cv.resize(image, (int(image.shape[1] * height / image.shape[0]), height))
contour_img = cv.resize(contour_img, (int(contour_img.shape[1] * height / contour_img.shape[0]), height))
img2 = cv.resize(img2, (int(img2.shape[1] * height / img2.shape[0]), height))
img3 = cv.resize(img3, (int(img3.shape[1] * height / img3.shape[0]), height))

# Combinez les images horizontalement
concatenated_image1 = np.hstack((image, contour_img))
concatenated_image2 = np.hstack(( img2, img3))
#cv.imshow('Detected Contours', concatenated_image1)
#cv.imshow('Detected Contours', concatenated_image2)
cv.imshow('Detected Contours', new_image)
cv.waitKey(0)
cv.destroyAllWindows()
cv.imwrite('processed_image.jpg', new_image)