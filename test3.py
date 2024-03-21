import cv2
import numpy as np
import math

def detect_circles(image_path): #image de base non modifiée
    img = cv2.imread(image_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 40, param1=90, param2=18, minRadius=15, maxRadius=24)

    circle_count = 0  
    circle_centers = []  
    circle_colors = []  
    distances = []  
    lines_info = []  
    intermediate_points = []  

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))

        for (x, y, r) in detected_circles[0, :]:
            roi = binary[y-r:y+r, x-r:x+r]
            mean_val = np.mean(roi)
            cv2.circle(output, (x, y), r, (0, 255, 0) if mean_val >= 50 else (255, 0, 0), 3)
            circle_centers.append((x, y, r))  
            circle_colors.append("white" if mean_val >= 50 else "black")  
            circle_count += 1  
            cv2.circle(output, (x, y), 3, (255, 0, 0), -1)
            intermediate_points.append((x, y))  # Ajouter les cercles détectés comme points intermédiaires

        print("Coordonnées des centres des cercles détectés:", circle_centers)
        print("Nombre total de cercles détectés:", circle_count)

        # Fusion des cercles proches
        while True:
            circles_merged = False  
            for i in range(len(circle_centers) - 1, 0, -1):
                for j in range(i - 1, -1, -1):  
                    x1, y1, r1 = circle_centers[i]
                    x2, y2, r2 = circle_centers[j]
                    dist_centers = np.sqrt((np.int64(x1) - np.int64(x2))**2 + (np.int64(y1) - np.int64(y2))**2)  
                    if dist_centers < 50:
                        new_x = int((x1 + x2) / 2)
                        new_y = int((y1 + y2) / 2)
                        new_r = int((r1 + r2) / 2)
                        circle_centers.append((new_x, new_y, new_r))
                        roi = binary[new_y-new_r:new_y+new_r, new_x-new_r:new_x+new_r]
                        mean_val = np.mean(roi)
                        circle_colors.append("white" if mean_val >= 50 else "black")
                        del circle_centers[i]
                        del circle_centers[j]
                        del circle_colors[i]
                        del circle_colors[j]
                        circle_count -= 1
                        circles_merged = True
                        break  
                if circles_merged:
                    break  
            if not circles_merged:
                break  

        print("Nombre de cercles après fusion:", circle_count)
        merged = circle_centers.copy()
        merged_colors = circle_colors.copy()
        print("Nouveaux cercles", merged)

        # Affichage des cercles fusionnés avec les couleurs appropriées
        merged_image = img.copy()
        output = cv2.resize(output, (800, 800))

        # Tracer les lignes entre les cercles alignés et calculer les distances
        for i in range(len(merged)):
            for j in range(i+1, len(merged)):
                x1, y1, _ = merged[i]
                x2, y2, _ = merged[j]
                # Si les cercles sont alignés verticalement
                if abs(int(x1) - int(x2)) < 50:
                    cv2.line(merged_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    distance = np.sqrt((np.int64(x2) - np.int64(x1))**2 + (np.int64(y2) - np.int64(y1))**2)
                    distances.append(distance)
                    lines_info.append(((x1, y1), (x2, y2)))  # Ajout des coordonnées des points pour cette ligne

                    # Calcul des points intermédiaires le long de la ligne
                    for k in range(1, 6):
                        x_intermediate = int(x1) + (int(x2) - int(x1)) * k / 6
                        y_intermediate = int(y1) + (int(y2) - int(y1)) * k / 6
                        intermediate_points.append((int(x_intermediate), int(y_intermediate)))  # Ajouter le point intermédiaire

                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 5, (255, 255, 0), -1)
                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 10, (0, 255, 255), -1)
                # Si les cercles sont alignés horizontalement
                elif abs(int(y1) - int(y2)) < 30:
                    cv2.line(merged_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    distance = np.sqrt((np.int64(x2) - np.int64(x1))**2 + (np.int64(y2) - np.int64(y1))**2)
                    distances.append(distance)
                    lines_info.append(((x1, y1), (x2, y2)))  # Ajout des coordonnées des points pour cette ligne

                    # Calcul des points intermédiaires le long de la ligne
                    for k in range(1, 6):
                        x_intermediate = int(x1) + (int(x2) - int(x1)) * k / 6
                        y_intermediate = int(y1) + (int(y2) - int(y1)) * k / 6
                        intermediate_points.append((int(x_intermediate), int(y_intermediate)))  # Ajouter le point intermédiaire

                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 10, (255, 255, 0), -1)
                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 10, (0, 255, 255), -1)
        while True:
            circles_merged = False  
            for i in range(len(intermediate_points) - 1, 0, -1):
                for j in range(i - 1, -1, -1):  
                    x1, y1 = intermediate_points[i]  
                    x2, y2 = intermediate_points[j] 
                    dist_centers = np.sqrt((np.int64(x1) - np.int64(x2))**2 + (np.int64(y1) - np.int64(y2))**2)  
                    if dist_centers < 50:
                        new_x = int((x1 + x2) / 2)
                        new_y = int((y1 + y2) / 2)
                        intermediate_points.append((new_x, new_y))  
                        del intermediate_points[i]  
                        del intermediate_points[j]  
                        circles_merged = True
                        break  
                if circles_merged:
                    break  
            if not circles_merged:
                break
        # Connecter les points sur les mêmes lignes horizontales et verticales
        #merged_image = connect_points_on_same_lines( merged_image, intermediate_points)

        # Affichage de l'image fusionnée avec les lignes connectées
        merged_image = cv2.resize(merged_image, (800, 800))
        cv2.imshow('output_and_merged_with_lines', merged_image)
        cv2.waitKey(0)
    
    print("Distances entre les points où les lignes sont tracées:", distances)
    print("Coordonnées des points utilisés pour les lignes tracées:", lines_info)
    print("intermediate points",len(intermediate_points))
    return output, circle_count, merged #output :

def connect_points_on_same_lines( merged_image, intermediate_points):
    # Définir une tolérance pour déterminer si deux points sont alignés
    tolerance = 20
    # Définir une distance minimale entre deux points pour tracer une ligne
    min_distance_x = 800
    min_distance_y = 800
    # Créer une liste pour stocker les lignes
    detected_lines = []
    # Compteur pour le nombre de points intermédiaires
    intermediate_points_count = 0
    # Parcourir tous les points
    for i in range(len(intermediate_points)):
        x1, y1 = intermediate_points[i]

        # Parcourir les autres points
        for j in range(i+1, len(intermediate_points)):
            x2, y2 = intermediate_points[j]
            # Vérifier si les points sont distincts
            if (x1, y1) != (x2, y2):
                # Calculer les distances en x et en y
                distance_x = abs(x2 - x1)
                distance_y = abs(y2 - y1)

                # Vérifier si les points sont alignés horizontalement et si la distance en y est suffisamment petite
                if distance_x < tolerance and distance_y >= min_distance_x:
                    # Ajouter les points à la liste des lignes
                    detected_lines.append(((x1, y1), (x2, y2)))

                # Vérifier si les points sont alignés verticalement et si la distance en x est suffisamment petite
                elif distance_y < tolerance and distance_x >= min_distance_y:
                    # Ajouter les points à la liste des lignes
                    detected_lines.append(((x1, y1), (x2, y2)))
    print("Nombre total de points intermédiaires:", len(intermediate_points))
    # Fusionner les lignes qui se chevauchent
    merged_lines = []
    for line1 in detected_lines:
        (x1, y1), (x2, y2) = line1
        add_line = True
        for line2 in merged_lines:
            (x3, y3), (x4, y4) = line2
            # Calculer les distances entre les points des deux lignes
            distance1 = math.sqrt((np.int64(x1) - np.int64(x3))**2 + (np.int64(y1) - np.int64(y3))**2)
            distance2 = math.sqrt((np.int64(x2) - np.int64(x4))**2 + (np.int64(y2) - np.int64(y4))**2)
            # Si l'une des extrémités de la ligne1 est très proche d'une des extrémités de la ligne2, ne pas ajouter la ligne1
            if distance1 < 2 or distance2 < 2:
                add_line = False
                break
        if add_line:
            merged_lines.append(line1)

    # Dessiner les lignes fusionnées sur l'image fusionnée
    for line in merged_lines:
        (x1, y1), (x2, y2) = line
        cv2.line(merged_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

        # Calcul des points intermédiaires le long de la ligne
        if math.sqrt((np.int64(x2) - np.int64(x1))**2 + (np.int64(y2) - np.int64(y1))**2) <= 1800:
            for k in range(1, 6):
                x_intermediate = int(x1) + (int(x2) - int(x1)) * k / 6
                y_intermediate = int(y1) + (int(y2) - int(y1)) * k / 6
                intermediate_points.append((int(x_intermediate), int(y_intermediate)))  # Ajouter le point intermédiaire
                # Incrémenter le compteur de points intermédiaires
                intermediate_points_count += 1

                cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 5, (255, 255, 0), -1)
                cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 10, (0, 255, 255), -1)

    # Afficher le nombre total de points intermédiaires
    print("Nombre total de points intermédiaires:", intermediate_points_count)

    # Afficher les coordonnées des lignes créées
    print("Coordonnées des lignes créées:")
    for i, line in enumerate(merged_lines):
        print(f"Ligne {i + 1}: {line}")

    return merged_image


img = "plateauideal.jpg"
detect_circles(img)
