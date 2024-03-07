import cv2
import numpy as np

def find_nearest_intersection(circle_center, intersections):
    """
    Trouve l'intersection la plus proche d'un cercle donné parmi la liste des intersections.
    Retourne les coordonnées de l'intersection la plus proche.
    """
    min_distance = float('inf')
    nearest_intersection = None

    for intersection in intersections:
        distance = np.sqrt((np.int64(circle_center[0]) - np.int64(intersection[0])) ** 2 + (np.int64(circle_center[1]) - np.int64(intersection[1])) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_intersection = intersection

    return nearest_intersection

def hough_transform(image_path):
    # Lire l'image en niveaux de gris
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 800))
    
    # Appliquer l'algorithme de Canny pour détecter les contours
    edges = cv2.Canny(image, 100, 200, apertureSize=3)  # Ajuster les seuils selon l'image
    
    # Afficher l'image en niveaux de gris
    cv2.imshow('Image en niveaux de gris', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Appliquer la transformée de Hough pour détecter les lignes
    lines = cv2.HoughLines(edges, 1, np.pi/180, 250)
    
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
                    if (0 <= intersection_point[0, 0] < image.shape[1]) and (0 <= intersection_point[1, 0] < image.shape[0]):
                        intersections.append((intersection_point[0, 0], intersection_point[1, 0]))  # Ajouter les coordonnées à la liste
                        cv2.circle(image, (int(intersection_point[0, 0]), int(intersection_point[1, 0])), 1, (0, 255, 0), -1)

    intersections_merge = []
    i = 0
    while i < len(intersections):
        x1, y1 = intersections[i]
        x1, y1 = int(x1), int(y1)
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
        
    intersection_count = len(intersections_merge)  # Compter les intersections détectées

    # Afficher l'image avec les lignes et les intersections détectées
    for x, y in intersections_merge:
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)

    # Afficher le nombre d'intersections détectées
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, f"Nombre d'intersections : {intersection_count}", (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # Afficher l'image
    cv2.imshow('Image avec intersections', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
        
    return intersections_merge

image_path ="4.jpg"
hough_transform(image_path)
