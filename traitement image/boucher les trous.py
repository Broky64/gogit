import cv2 as cv
import numpy as np

def contour_max(contours,indice):
    biggest = np.array([])
    max_area=0
    compteur=0
    for i in range (len(contours)):
        area = cv.contourArea(contours[i])
        if area > 0 and i not in indice:
            peri = cv.arcLength(contours[i], True)
            approx = cv.approxPolyDP(contours[i], 0.2 * peri, True)
            if area > max_area :
                compteur+=1
                biggest = approx
                max_area = area
                M = cv.moments(contours[i])
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                indice.append(i)
    return indice


def boucher_trous(image,indice):
    
     # Charger l'image

    # cv.imshow('Detected Contours', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    
    img1=image.copy()
    img2=image.copy()
    img3=image.copy()


    # Convertir l'image en niveaux de gris
    gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

    # # Appliquer un seuillage adaptatif
    #thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)
    _, thresh = cv.threshold(gray, 140, 255, cv.THRESH_BINARY)

    cv.imshow('Detected Contours', thresh)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Appliquer une détection de contours
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img3, contours, -1, 255, -1)
    cv.imshow('Image avec les trous bouchés', img3)
    cv.waitKey(0)
    cv.destroyAllWindows()
        # Sélectionner le plus grand contour
        # trouver l'aire la plus grande et les coins de cette aire
    
        # Dessiner les contours détectés sur une image vide
    contour_img = np.zeros_like(img1)

    indice=contour_max(contours,indice)
    largest_contour = contours[indice[-1]]
    # Approximer le contour par un polygone
    epsilon = 0.015 * cv.arcLength(largest_contour, True)
    approx = cv.approxPolyDP(largest_contour, epsilon, True)
    print(len(approx))
    # Si le polygone a 4 côtés (approximation d'un rectangle)
    if len(approx) < 8:
        mask = np.zeros_like(gray)
        cv.drawContours(mask, contours[indice[-1]], -1, 255, -1)
        
        cv.imshow('Detected Contours', mask)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return True
    else:
        boucher_trous(image,indice)
        return False
    
    # Dilater le masque pour remplir les trous
    kernel = np.ones((5,5),np.uint8)
    filled_mask = cv.dilate(mask, kernel, iterations=2)
    
    # Appliquer le masque rempli à l'image d'origine
    result = cv.inpaint(image, filled_mask, inpaintRadius=3, flags=cv.INPAINT_TELEA)
    return result

# Charger l'image
image = cv.imread('plateau_pied.jpg')
hauteur, largeur, canaux = image.shape
print(hauteur,largeur)
hauteur1=int(hauteur*(8000/hauteur)/10)
largeur1=int(largeur*(6000/largeur)/10)
print(hauteur1,largeur1)
image = cv.resize(image, (hauteur1,largeur1), 0.5, 0.5)
indice = []
# Appeler la fonction pour boucher les trous
image_bouchee = boucher_trous(image,indice)
print(image_bouchee)
# Afficher l'image originale et l'image avec les trous bouchés
cv.imshow('Image originale', image)
cv.imshow('Image avec les trous bouchés', image_bouchee)
cv.waitKey(0)
cv.destroyAllWindows()
