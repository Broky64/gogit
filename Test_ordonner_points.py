import cv2
import numpy as np
from detection_cercle import detect_circles

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

def label_intersections(intersections): #intersections : liste des intersections
    """
    Numérote chaque intersection de aa pour tout en haut à gauche jusqu'à tt pour tout en bas à droite.
    Retourne un dictionnaire avec les étiquettes et les coordonnées des intersections.
    """
    labels_dict = {}
    label_index = 0
    for i in range(19):  # Augmenter la taille de la grille pour contenir plus d'intersections
        for j in range(19):  # Augmenter la taille de la grille pour contenir plus d'intersections
            if label_index < len(intersections):
                label = chr(97 + j) + chr(97 + i)  # Convertir les indices en lettres
                labels_dict[label] = intersections[label_index]  # Associer l'étiquette aux coordonnées
                label_index += 1
    print("labels_dict",labels_dict)
    return labels_dict #labels_dict : liste avec les coordonnées et leur lettre associé du goban 

def sort_intersections(intersections): #intersections : liste des intersections dans le désordre
    """
    Trie les intersections en fonction de leur position en x et y.
    """
    return sorted(intersections, key=lambda x: (round(x[1]/14)*14, round(x[0]))) #liste avec les intersections triées


def hough_transform(image_path): #image_path : photo du plateau non modifiées
    # Lire l'image en niveaux de gris
    output, circle_count, circle_list, merged_colors = detect_circles(image_path)
    image = cv2.imread(image_path)
    q, s, d = image.shape
    image = cv2.resize(image, (800, 800))
    k, l, m = image.shape
    w = q / k  # calcul de la différence de width entre les 2 images
    h = s / l  # calcul de la différence de hight entre les 2 images
    c = d / m

    # Appliquer l'algorithme de Canny pour détecter les contours
    edges = cv2.Canny(image, 50, 200, apertureSize=3)  # Ajuster les seuils selon l'image

    # Afficher l'image en niveaux de gris
    cv2.imshow('Image en niveaux de gris', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Appliquer la transformée de Hough pour détecter les lignes
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 250)

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
            for j in range(i + 1, len(lines)):
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
                        cv2.circle(image, (int(intersection_point[0, 0]), int(intersection_point[1, 0])), 5, (0, 255, 0), -1)

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

    # Trier les intersections avant de les étiqueter
    intersections_merge = sort_intersections(intersections_merge)

    # Afficher l'image des intersections
    intersections_image = np.zeros_like(output)
    for x, y in intersections_merge:
        cv2.circle(intersections_image, (int(x), int(y)), 5, (0, 255, 0), -1)
    cv2.imshow('Image des intersections', intersections_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Numéroter les intersections
    intersections_labeled = label_intersections(intersections_merge)
    print("Intersections étiquetées :")
    print(intersections_labeled)

    # Afficher le nombre d'intersections détectées
    font = cv2.FONT_HERSHEY_SIMPLEX
    print("nombre d'intersections :", intersection_count)
    print("nombre de cercle :", circle_count)

    # Créer une image vide pour dessiner les intersections
    intersections_image = np.zeros_like(output)

    # Dessiner les intersections sur l'image vide
    for x, y in intersections_merge:
        cv2.circle(intersections_image, (int(x), int(y)), 5, (0, 255, 0), -1)

    # Superposer les cercles détectés avec les intersections
    output_with_intersections = cv2.addWeighted(output, 0.5, intersections_image, 0.5, 0)
    for label, intersection_coords in intersections_labeled.items():
        x, y = intersection_coords
        text = f"({int(x)}, {int(y)})"
        cv2.putText(output_with_intersections, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255),
                    1, cv2.LINE_AA)
    # Afficher l'image superposée

    cv2.imshow('Images superposées', output_with_intersections)

    # Trouver l'intersection la plus proche de chaque cercle et l'afficher
    intersections_near_circles = []  # Liste pour stocker les informations sur les intersections près des cercles

    for circle_center, circle_color in zip(circle_list, merged_colors):
        # Diviser les coordonnées des cercles par les facteurs de redimensionnement
        circle_center_resized = (circle_center[0] / h, circle_center[1] / w)
        nearest_intersection = find_nearest_intersection(circle_center_resized, intersections_merge)

        # Trouver la lettre associée à l'intersection
        for label, intersection_coords in intersections_labeled.items():
            if intersection_coords == nearest_intersection:
                intersection_label = label
                break

        # Ajouter les informations sur l'intersection, y compris la couleur du cercle
        intersections_near_circles.append((nearest_intersection, intersection_label, circle_color))

    # Affichage des intersections près des cercles avec leurs informations
    print("Intersections près des cercles avec leurs informations :")
    for intersection_info in intersections_near_circles:
        print("Intersection:", intersection_info[0], "Lettres associées:", intersection_info[1],
              "Couleur du cercle:", intersection_info[2])
    print("width:", w)
    print("high:", h)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("intersections_near_circles",intersections_near_circles)
    return intersections_near_circles #liste avec les coordonnées du centre de la pierre, les 2 lettres de lignes et colonnes associées, la couleur de la pirre
image_path = "processed_image.jpg"
hough_transform(image_path)
