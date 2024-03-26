import cv2
import numpy as np
# ==============================================================================
# sous fonction
# ==============================================================================

# ------------------------------------------------------------------------------
# comparairaison d'aire entrecoins 
# ------------------------------------------------------------------------------
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


# def points_equidistant(biggest, center_x,center_y):
#     #d'abord il faut regroupé les points proches entre eux
#     points_proches = []
#     biggest = biggest.reshape(-1, 2)
#     #print('biggest',biggest, 'area',max)
#     list_indice=[]
#     for i in range (len(biggest)):
#         if i not in list_indice:
#             list_médian=[]
#             x1 ,y1 = biggest[i]
#             #cv.circle(contour_img, (x1, y1), 15, (0, 255, 255), -1)
#             list_médian.append([x1, y1])
#             for j in range(i+1,len(biggest)):
#                 x2 ,y2 = biggest[j]
#                 distance = ((x2-x1)**2+(y2-y1)**2)**(1/2)
#                 if distance < 50:
#                     list_indice.append(j)
#                     list_médian.append([x2,y2])
#             points_proches.append(list_médian)
#     print('points_proches',points_proches)

#     #puis trouver le points le plus proche du barycentre dans chaque groupe
#     distance_centre=[]
#     points_equidistant = []
#     for elem in points_proches:
#         x, y = elem
#         distance = ((center_x - x) ** 2 + (center_y - y) ** 2) ** (1 / 2)
#         distance_centre.append(distance)
#     for i in range (len(distance_centre)):
#         eq_dist = [distance_centre[i]]
#         index_coins=[i]
#         for j in range (i+1,len(distance_centre)):
#             if abs(distance_centre[i]-distance_centre[j])<30:
#                 eq_dist.append(distance_centre[j])
#                 index_coins.append(j)
#             if len(eq_dist) == 4:
#                 for index in index_coins:
#                     points_equidistant.append(points_proches[index])
#     return points_equidistant
# biggest =[[[ 96, 237]]

#  [[429, 257]]

#  [[149, 609]]

#  [[680, 615]]

#  [[668, 279]]

#  [[684, 619]]

#  [[145, 613]]

#  [[180, 259]]

#  [[418, 628]]

#  [[127, 632]]

#  [[698, 632]]

#  [[418, 628]]

#  [[647, 251]]]
# center_x=417
# center_y=442
# result=points_equidistant(biggest,417,442)

def points_correctes(biggest, aire_cherchée):
    aire=0
    diff = proche_aire(aire,aire_cherchée)
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


def distance_entre_points(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

def eliminer_lignes_superposees(lines, seuil_distance):
    lines_a_garder = []
    for i in range(len(lines)):
        is_superposee = False
        for j in range(i + 1, len(lines)):
            distance = min(distance_entre_points(lines[i][0][:2], lines[j][0][:2]),
                           distance_entre_points(lines[i][0][:2], lines[j][0][2:]),
                           distance_entre_points(lines[i][0][2:], lines[j][0][:2]),
                           distance_entre_points(lines[i][0][2:], lines[j][0][2:]))
            if distance < seuil_distance:
                is_superposee = True
                break
        if not is_superposee:
            lines_a_garder.append(lines[i])
    return lines_a_garder

# def lignes_superposees(lines):
#     lines_a_garder=[]
#     for i in range(len(lines)):
#         for j in range(i+1, len(lines)):
#             x1, y1 = lines[i][0]
#             x2, y2 = lines[j][0]
#             coef1= abs((y2-y1)/(x2-x1))
#         for k in range(len(lines)):
#             if k!=i and k!=j:
#                 for l in range(i+1,len(lines)):
#                     if l!=i and l!=j:
#                         x3, y3 = lines[k][0]
#                         x4, y4 = lines[l][0]
#                         coef2= abs((y4-y3)/(x4-x3))
#                         if abs(coef2-coef1)<1:
#                             k=coef1
#         return k