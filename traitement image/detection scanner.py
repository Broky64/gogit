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

    image = cv.imread('plateau_pied3.jpg')
    #image= cv.imread('pierres1.jpg')

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

    # Appliquer une détection de contours
    contours, _ = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    contour_img1 = np.zeros_like(img1)
    cv.drawContours(contour_img1, contours, -1, (255, 255, 255), 2)
    cv.imshow('contours', contour_img1)
    cv.waitKey(0)
    cv.destroyAllWindows()

    contours = sorted(contours,key=cv.contourArea,reverse=True)[:5]
    for c in contours:
        peri = cv.arcLength(c,True)
        approx = cv.approxPolyDP(c,0.02*peri,True)
        if len(approx)==4:
            doc = approx
            break

    bons_coins=[]
    for d in doc:
        tuple_point = tuple(d[0])
        cv2.circle(img2,tuple_point,3,(0,0,255),4)
        bons_coins.append(tuple_point)
    cv2.imshow('Corner points detected',img2)
    cv2.waitKey(0)


    bons_coins = sorted(bons_coins, key=lambda coord:coord[0])
    bons_coins[:2] = sorted(bons_coins[:2],key=lambda coord:coord[1])
    bons_coins[2:] = sorted(bons_coins[2:],key=lambda coord:coord[1])


    points_ordre = bons_coins

    x1, y1 = points_ordre[0]
    x2, y2 = points_ordre[1]
    x3, y3 = points_ordre[2]
    x4, y4 = points_ordre[3]
    print('points_ordre', points_ordre)


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

    cv.imshow('recadrage', new_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return new_image


cadrage=separation_objet_image()