import numpy as np
import cv2 as cv
from scipy.spatial.distance import cdist
import math
import itertools
from fonction_séparation import *
# import Image module
from PIL import Image

# ==============================================================================
# fonction principale
# ==============================================================================


def separation_objet_image():

    # Charger l'image

    image = cv.imread('plateau_pied.jpg')
    image= cv.imread('pierres1.jpg')

    # cv.imshow('Detected Contours', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    hauteur, largeur, canaux = image.shape
    print(hauteur,largeur)
    hauteur1=int(hauteur*(8000/hauteur)/10)
    largeur1=int(largeur*(6000/largeur)/10)
    print(hauteur1,largeur1)
    image = cv.resize(image, (hauteur1,largeur1), 0.5, 0.5)


    img1=image.copy()
    img2=image.copy()
    img3=image.copy()
    img4=image.copy()
    img5=image.copy()


    # Convertir l'image en niveaux de gris
    gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

    # convertir en flou
    blur= cv.GaussianBlur(gray,(9,9),0)
    
    cv.imshow('blur', blur)
    cv.waitKey(0)
    cv.destroyAllWindows()

    edge=cv.Canny(blur,75,200, apertureSize=3)
    cv.imshow('edge', edge)
    cv.waitKey(0)
    cv.destroyAllWindows()

    #  Appliquer un seuillage adaptatif
    thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
    #_, thresh = cv.threshold(blur, 140, 255, cv.THRESH_BINARY)

    cv.imshow('tresh', thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()




    # Appliquer une détection de contours
    contours, _ = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    


    # trouver l'aire la plus grande et les coins de cette aire
    biggest = np.array([])
    max_area=0
    compteur=0
    for i in range (len(contours)):
        area = cv.contourArea(contours[i])
        if area > 0:
            peri = cv.arcLength(contours[i], True)
            approx = cv.approxPolyDP(contours[i], 0.02 * peri, True)
            if area > max_area :
                compteur+=1
                biggest = approx
                max_area = area
                M = cv.moments(contours[i])
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                indice=i
    
    # Dessiner les contours détectés sur une image vide
    contour_img = np.zeros_like(img1)
    cv.drawContours(contour_img, contours[indice], -1, (255, 255, 255), 2)

    cv.imshow('Detected Contours', contour_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    contour_img = cv.cvtColor(contour_img, cv.COLOR_BGR2GRAY)

    # Convertir l'image en binaire
    # _, contour_thresh = cv.threshold(contour_img, 180, 255, cv.THRESH_BINARY)
    # contour_blur= cv.GaussianBlur(contour_thresh,(5,5),0)

    # cv.imshow('Detected Contours', contour_blur)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


    # Trouver les lignes dans les contours avec la transformée de Hough
    lines = cv.HoughLinesP(contour_blur, rho=4, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    # print('line',lines[2][0])
    # x1, y1, x2, y2= lines[][0]
    # cv.line(img5, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # cv.circle(img5, ( x1,y1), 15, (0, 255, 255), 5)
    # cv.circle(img5, ( x2,y2), 15, (0, 255, 255), 5)
    # cv.imshow('Detected Contours', img5)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
        
    # Appel de la fonction pour éliminer les lignes superposées
    seuil_distance = 10  # Ajustez ce seuil en fonction de vos besoins
    lines_filtrees = eliminer_lignes_superposees(lines, seuil_distance)

    # Dessiner les lignes sur une copie de l'image originale
    line_image = image.copy()
    print('nbre_ligne',len(lines))
    print('nbre_ligne_merge',len(lines_filtrees))
    for i in range (len(lines_filtrees)):
        x1, y1, x2, y2 = lines_filtrees[i][0]
        cv.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 4)
    
    # Trouver les intersections des lignes
    intersections = cv.bitwise_and(image, line_image)
    cv.imshow('Detected Contours', intersections)
    cv.waitKey(0)
    cv.destroyAllWindows()



    intersections = []

    for i in range(len(lines_filtrees)):
        for j in range(i+1, len(lines_filtrees)):
            lines_filtrees1 = lines_filtrees[i][0]
            lines_filtrees2 = lines_filtrees[j][0]

            # Trouver le point d'intersection entre les deux lignes
            x1, y1 = lines_filtrees1[0], lines_filtrees1[1]
            x2, y2 = lines_filtrees1[2], lines_filtrees1[3]
            x3, y3 = lines_filtrees2[0], lines_filtrees2[1]
            x4, y4 = lines_filtrees2[2], lines_filtrees2[3]

            denom = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

            if denom != 0:
                x = (((x1*y2 - y1*x2) * (x3 - x4)) - ((x1 - x2) * (x3*y4 - y3*x4))) / denom
                y = (((x1*y2 - y1*x2) * (y3 - y4)) - ((y1 - y2) * (x3*y4 - y3*x4))) / denom

                # Vérifier si le point d'intersection se trouve à l'intérieur de l'image
                if 0 <= x <= img3.shape[1] and 0 <= y <= img3.shape[0]:
                    intersections.append((int(x), int(y)))

    print('nbrre_intersections',len(intersections))

    for elem in intersections:
        x, y = elem
        cv.circle(img3, (x, y), 15, (0, 0, 255), 5)

    cv.imshow('coin', img3)
    cv.waitKey(0)
    cv.destroyAllWindows()
    print('nbre_intersections',len(intersections))
    bons_coins = intersections
 
#     top = max(contours[indice], key=lambda point: point[0][0])[0][0]
#     bottom = min(contours[indice], key=lambda point: point[0][0])[0][0]
#     right = max(contours[indice], key=lambda point: point[0][1])[0][1]
#     left = min(contours[indice], key=lambda point: point[0][1])[0][1]
#     print('top',top, bottom,right, left)
#     h=top-bottom
#     l=right-left
    
#     cv.circle(img2, ( top,right), 15, (0, 255, 255), 5)
#     cv.circle(img2, ( top,left), 15, (0, 255, 255), 5)
#     cv.circle(img2, ( bottom,right), 15, (0, 255, 255), 5)
#     cv.circle(img2, ( bottom,left), 15, (0, 255, 255), 5)
    
#     for elem in biggest:
#         x, y = elem[0]
#         cv.circle(img1, (x, y), 15, (0, 0, 255), 5)
    
    
#     cv.imshow('coin', img1)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     #plus_grand=max(contours, key=cv.contourArea)
#     #cv.drawContours(contour_img, plus_grand, -1, (0, 255, 0), 2)
#     #print(compteur)
                

#     cv.circle(img2, (center_x, center_y), 15, (255, 0, 255), -1)
#     cv.imshow('points extrémité', img2)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     img3 = img3[left : left+l,bottom : bottom-h ]
#     cv.imshow('rognement', img3)
#     cv.waitKey(0)
#     cv.destroyAllWindows()



# # ==============================================================================
# # on étudie l'image rogner
# # ==============================================================================
#     # Convertir l'image en niveaux de gris
#     gray = cv.cvtColor(img3, cv.COLOR_BGR2GRAY)
#     blur= cv.GaussianBlur(gray,(5,5),1)
#     # # Appliquer un seuillage adaptatif
#     cv.imshow('blur', blur)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
#     #_, thresh = cv.threshold(blur, 140, 255, cv.THRESH_BINARY)

#     cv.imshow('tresh', thresh)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

#     contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
#     #cut cropp
    
#     # Dessiner les contours détectés sur une image vide
#     contour_img = np.zeros_like(img3)

#     # trouver l'aire la plus grande et les coins de cette aire
#     biggest = np.array([])
#     max_area=0
#     compteur=0
#     for i in range (len(contours)):
#         area = cv.contourArea(contours[i])
#         if area > 0:
#             peri = cv.arcLength(contours[i], True)
#             approx = cv.approxPolyDP(contours[i], 0.2 * peri, True)
#             if area > max_area :
#                 compteur+=1
#                 biggest = approx
#                 max_area = area
#                 M = cv.moments(contours[i])
#                 center_x = int(M["m10"] / M["m00"])
#                 center_y = int(M["m01"] / M["m00"])
#                 indice=i



#     for elem in biggest:
#         x, y = elem[0]
#         cv.circle(img3, (x, y), 15, (0, 0, 255), 5)
    
    
#     cv.imshow('coin', img3)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
   


    
#     cv.drawContours(mask, contours[indice], -1, (255,255,0), -1)
#     cv.imshow('mask', mask)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#    # masked_image = cv.bitwise_and(image, image, mask)
    
#     # Appliquer le masque pour conserver l'intérieur du contour
#     inside_contour = cv.bitwise_and(image, image, mask=mask)
#     cv.imshow('inside', inside_contour)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     # Créer une image noire de même taille que l'image originale
#     black_image = np.zeros_like(image) 
#     outside_contour=cv.bitwise_not(mask)

#     outside_contour = cv.bitwise_and(black_image, black_imageimage, mask=outside_contour)
#     cv.imshow('outside', outside_contour)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

#     final_image = cv.add(inside_contour, outside_contour)
#     cv.imshow('outside', final_image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#     # Copier le plus grand contour sur l'image noire
#     #masked_image = np.where(mask != 0, image, black_image)
#     #masked_image = np.where(mask[...,None] != 0, image, mask)
   

#     points_proches = []
#     etat=False
#     biggest = biggest.reshape(-1, 2)
#     print('biggest',biggest, 'area',max)
#     list_indice=[]
#     for i in range (len(biggest)):
#         if i not in list_indice:
#             List_médian=[]
#             x1 ,y1 = biggest[i]
#             #cv.circle(contour_img, (x1, y1), 15, (0, 255, 255), -1)
#             List_médian.append([x1, y1])
#             for j in range(i+1,len(biggest)):
#                 x2 ,y2 = biggest[j]
#                 distance = ((x2-x1)**2+(y2-y1)**2)**(1/2)
#                 if distance < 50:
#                     list_indice.append(j)
#                     List_médian.append([x2,y2])
#             points_proches.append(List_médian)
#     print('points_proches',points_proches)

#     points_correctes = []
#     for i in range(len(points_proches)):
#         min_distance = float('inf')  # Réinitialisation de la distance minimale pour chaque sous-liste de points
#         if len(points_proches[i]) > 1:
#             indice=0
#             for j in range(len(points_proches[i])):
#                 point = points_proches[i][j]
#                 x0, y0 = point
#                 distance = ((center_x - x0) ** 2 + (center_y - y0) ** 2) ** (1 / 2)
#                 if distance < min_distance or j == 0:
#                     min_distance = distance
#                     indice = j
#             points_correctes.append(points_proches[i][indice])
#         else:
#             points_correctes.append(points_proches[i][0])
#     print(points_correctes)


# # trouver points à equidistance(+ ou -) du barycentre de la plus grande aire 
#     distance_centre=[]
#     index_coins= []
#     bons_coins=[]
#     for elem in points_correctes:
#         x, y = elem
#         distance = ((center_x - x) ** 2 + (center_y - y) ** 2) ** (1 / 2)
#         distance_centre.append(distance)
#     for i in range (len(distance_centre)):
#         eq_dist = [distance_centre[i]]
#         index_coins=[i]
#         for j in range (i+1,len(distance_centre)):
#             if abs(distance_centre[i]-distance_centre[j])<50:
#                 eq_dist.append(distance_centre[j])
#                 index_coins.append(j)
#         if len(eq_dist) ==4:
#             for index in index_coins:
#                 bons_coins.append(points_correctes[index])
#     for elem in bons_coins:
#         x, y = elem
#         cv.circle(img3, (x, y), 15, (0, 0, 255), -1)
        

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
    cv.circle(img4, (x1, y1), 15, (0, 0, 255), 1)
    cv.imshow('Detected Contours', img4)
    cv.waitKey(0)
    cv.destroyAllWindows()
    pts_source = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)

    # Définir les nouvelles positions des coins après la transformation
    # Par exemple, pour une sortie de taille fixe, vous pouvez utiliser :
    width = 800  # Largeur de l'image de sortie
    height = 800  # Hauteur de l'image de sortie
    pts_destination = np.array([[0, 0], [width, 0], [0, height], [width, height]], dtype=np.float32)

    # Calculer la matrice de transformation de perspective
    matrix = cv.getPerspectiveTransform(pts_source, pts_destination)

    # Appliquer la transformation de perspective à l'image d'origine
    new_image = cv.warpPerspective(image, matrix, (width, height),flags=cv.INTER_LINEAR)

    # # Redimensionner les images pour qu'elles aient la même hauteur
    # height = min(image.shape[0], contour_img.shape[0], img2.shape[0], img3.shape[0])
    # image = cv.resize(image, (int(image.shape[1] * height / image.shape[0]), height))
    # contour_img = cv.resize(contour_img, (int(contour_img.shape[1] * height / contour_img.shape[0]), height))
    # img2 = cv.resize(img2, (int(img2.shape[1] * height / img2.shape[0]), height))
    # img3 = cv.resize(img3, (int(img3.shape[1] * height / img3.shape[0]), height))

    # Combinez les images horizontalement

    #concatenated_image1 = np.hstack((image, contour_img))

    # concatenated_image2 = np.hstack(( img2, img3))
    #cv.imshow('Detected Contours', image)
    # cv.imshow('Detected Contours', concatenated_image2)
    cv.imshow('Detected Contours', new_image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return new_image

new_image=separation_objet_image()
