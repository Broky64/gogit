import cv2
import numpy as np


def hough_transform(image_path):
    # Lire l'image en niveaux de gris
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 800))
    
    # Appliquer l'algorithme de Canny pour détecter les contours
    edges = cv2.Canny(image, 100, 200, apertureSize=3)  # Ajuster les seuils selon l'image
    
    # Appliquer la transformée de Hough pour détecter les lignes
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    
    # Initialiser le compteur d'intersections
    intersection_count = 0
    intersections = []  # Liste pour stocker les coordonnées des intersections
    
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        # Trouver les intersections entre les lignes détectées
        for i in range(len(lines)):
            for j in range(i+1, len(lines)):
                rho1, theta1 = lines[i][0]
                rho2, theta2 = lines[j][0]
                denominator = np.sin(theta1 - theta2)
                if denominator != 0:  # Vérifier que le dénominateur n'est pas égal à zéro
                    A = np.array([
                        [np.cos(theta1), np.sin(theta1)],
                        [np.cos(theta2), np.sin(theta2)]
                    ])
                    b = np.array([[rho1], [rho2]])
                    intersection_point = np.linalg.solve(A, b)
                    if (0 <= intersection_point[0] < image.shape[1]) and (0 <= intersection_point[1] < image.shape[0]):
                        intersections.append((intersection_point[0], intersection_point[1]))  # Ajouter les coordonnées à la liste
                        cv2.circle(image, (int(intersection_point[0]), int(intersection_point[1])), 5, (0, 255, 0), -1)

    intersections_merge = []
    i = 0
    while i < len(intersections):
        x1, y1 = intersections[i]
        x1, y1 =int(x1),int(y1)
        j = i + 1
        while j < len(intersections):
            x2, y2 = intersections[j]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if distance < 20:
                x1 = int((x1 + x2) / 2) 
                y1 = int((y1 + y2) / 2)
                del intersections[j]
            else:
                j += 1
        intersections_merge.append((x1, y1))
        
        i += 1
        


    # Afficher l'image avec les lignes et les intersections détectées
    #for x, y in intersections_merge:
        #cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    intersections_merge=sorted(intersections_merge, key=lambda coord: (-coord[1], coord[0]))
    for i in range (len(intersections_merge)):
        x1 , y1 = intersections_merge[i]
        x2, y2 = intersections_merge[i-1]
        if abs(y1-y2)<5:
            intersections_merge[i]=x1, y2
        
    return sorted(intersections_merge, key=lambda coord: (-coord[1], coord[0]))

def cercle(image_path):
    niveau_gris_intersections=[]
    intersections_merge=hough_transform(image_path)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 800))
    
    for k in range(len(intersections_merge)):
        x, y = intersections_merge[k]
        ordonnée=k//19
        abscisse=k-ordonnée*19
        niveau_gris_pixel=[]
        #print(x,y, abscisse, ordonnée)
        #cv2.circle(image, (x,y), radius=15, color=(0, 0, 255), thickness=-1)

        # Créer un masque circulaire
        for i in range(y-15, y+15):
            for j in range(x-15, x+15):
                gris = int(0.2126 * image[i][j][0] + 0.7152 * image[i][j][1] + 0.0722 * image[i][j][2])
                niveau_gris_pixel.append(gris)
        intensité_gris_zone = np.mean(niveau_gris_pixel)
        #print(intensité_gris_zone,abscisse,ordonnée)
        cv2.circle(image, (x,y), radius=15, color=(intensité_gris_zone, intensité_gris_zone, intensité_gris_zone), thickness=-1)
        niveau_gris_intersections.append(intensité_gris_zone)

    #print(niveau_gris_intersections)
    
    cv2.imshow("niveaux de gris intersections", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return niveau_gris_intersections

def etat_position(image_path):
    niveau_gris_intersections=cercle(image_path)
    tableau_etat=[]
    i=0
    for moy in range (len(niveau_gris_intersections)):
        ordonnée=i//19
        abscisse=i-ordonnée*19
        if 140<niveau_gris_intersections[i]<160:
            etat="EM"
        elif 140>niveau_gris_intersections[i]:
            etat="B"
        else:
            etat="W"
        tableau_etat.append((abscisse,ordonnée,etat))
        i+=1
        print(abscisse,ordonnée,etat)
    
    return tableau_etat



#image_path="1plateau.jpg"
#image_path="plateauideal.jpg"
image_path="goban.png"
#niveau_gris_intersections = cercle(image_path)
tableau=etat_position(image_path)