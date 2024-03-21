import cv2
import numpy as np
from detection_cercle import detect_circles
img="processed_image3.jpg"
def find_nearest_intersection(circle_center, intersections): #circle_center : centre des pierres détectées, intersections : liste des intersections détectées
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
    return nearest_intersection  #coordonnée de l'intersection la plus proche de la pierre cherchée

def goban(image_path): 
    image = cv2.imread(image_path)

    # Définir le nombre de lignes et de colonnes
    nb_lignes = 19
    nb_colonnes = 19

    # Obtenir les dimensions de l'image
    hauteur, largeur, _ = image.shape

    # Initialiser une liste pour stocker les coordonnées des intersections
    coordonnees_intersections = []

    # Calculer les intervalles entre les lignes et les colonnes
    intervalles_lignes = (hauteur - 1) // (nb_lignes - 1)
    intervalles_colonnes = (largeur - 1) // (nb_colonnes - 1)

    # Parcourir chaque intersection et stocker ses coordonnées
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            x = j * intervalles_colonnes
            y = i * intervalles_lignes
            coordonnees_intersections.append((x, y))

    # Afficher le nombre total d'intersections
    nb_intersections = len(coordonnees_intersections)
    print("Nombre total d'intersections :", nb_intersections)

    # Afficher les coordonnées des intersections
    print("Coordonnées des intersections :")
    for intersection in coordonnees_intersections:
        print(intersection)

    # Tri et étiquetage des intersections
    intersections_triees = sort_intersections(coordonnees_intersections)
    intersections_etiquetees = label_intersections(intersections_triees)

    # Dessiner les lignes
    for i in range(nb_colonnes):
        x = i * intervalles_colonnes
        cv2.line(image, (x, 0), (x, hauteur), (0, 255, 0), 1)

    for i in range(nb_lignes):
        y = i * intervalles_lignes
        cv2.line(image, (0, y), (largeur, y), (0, 255, 0), 1)

    # Afficher l'image avec les lignes dessinées
    cv2.imshow('Image avec lignes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    _, _, merged, color = detect_circles(image_path)
    resultats = []

    for circle_center, circle_color in zip(merged, color):
        nearest_intersection = find_nearest_intersection(circle_center, intersections_etiquetees.values())
        if nearest_intersection:
            for label, coord in intersections_etiquetees.items():
                if coord == nearest_intersection:
                    resultats.append((circle_center, label, circle_color))
                    break

    print("Résultats :", resultats)
    return intersections_etiquetees, resultats

def label_intersections(intersections): 
    labels_dict = {}
    label_index = 0
    for i in range(19):  
        for j in range(19):  
            if label_index < len(intersections):
                label = chr(97 + j) + chr(97 + i)  
                labels_dict[label] = intersections[label_index]  
                label_index += 1
    print("labels_dict", labels_dict)
    return labels_dict

def sort_intersections(intersections): 
    return sorted(intersections, key=lambda x: (round(x[1]/14)*14, round(x[0])))

goban(img)