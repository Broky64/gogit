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
    for x, y in intersections_merge:
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)
    cv2.imshow("transformation de hough", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #print(sorted(intersections_merge, key=lambda coord: (coord[1], coord[0])))
    print(len(intersections_merge))
    return intersections_merge

def cercle(image_path):
    niveau_gris_intersections=[]
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 800))
    intersections_merge=hough_transform(image_path)
    for i in range(len(intersections_merge)):
        x, y = intersections_merge[i]
        ordonnée=i//19
        abscisse=i-ordonnée*19
        # Créer un masque circulaire
        masque_cercle = np.zeros_like(image)
        
        cv2.circle(masque_cercle, (x, y), 13, 255, -1)
        
        # Appliquer le masque à l'image et calculer la moyenne des valeurs de pixels dans le cercle
        pixels_dans_cercle = cv2.bitwise_and(image, masque_cercle)

        moyenne_pixels_dans_cercle = np.mean(pixels_dans_cercle)
        niveau_gris_intersections.append((moyenne_pixels_dans_cercle,abscisse, ordonnée))
    print(niveau_gris_intersections)
    return niveau_gris_intersections

def etat_position(niveau_gris_intersections):
    tableau_etat=[]
    i=0
    for moy, x, y in range (len(niveau_gris_intersections)):
        ordonnée=i//19
        abscisse=i-ordonnée*19
        if 0.023<niveau_gris_intersections[i]<0.03:
            etat="EM"
        elif 0.03<niveau_gris_intersections[i]:
            etat="B"
        else:
            etat="W"
        tableau_etat.append((abscisse,ordonnée,etat))
        i+=1
    print (tableau_etat)
    return tableau_etat
        
        
            


image_path="pierres1.jpg"
#image_path="plateauideal.jpg"
#image_path="goban.png"
niveau_gris_intersections = cercle(image_path)
#etat_position(niveau_gris_intersections)