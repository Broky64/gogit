import cv2
import numpy as np

def detect_circles(image_path): 
    img = cv2.imread(image_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 40, param1=90, param2=18, minRadius=15, maxRadius=24)

    circle_count = 0  
    circle_centers = []  
    circle_colors = []  
    distances = []  # Liste pour stocker les distances entre les points
    lines_info = []  # Liste pour stocker les informations sur les lignes tracées

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))

        for (x, y, r) in detected_circles[0, :]:
            roi = binary[y-r:y+r, x-r:x+r]
            mean_val = np.mean(roi)
            cv2.circle(output, (x, y), r, (0, 255, 0) if mean_val >= 50 else (255, 0, 0), 3)
            circle_centers.append((x, y, r))  
            circle_colors.append("blanc" if mean_val >= 50 else "noir")  
            circle_count += 1  
            cv2.circle(output, (x, y), 3, (255, 0, 0), -1)

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
                        circle_colors.append("blanc" if mean_val >= 50 else "noir")
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
        print("nouveaux cercles", merged)

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
                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 5, (255, 255, 0), -1)

                        # Ajout des cercles de rayon 10 pixels
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
                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 10, (255, 255, 0), -1)

                        # Ajout des cercles de rayon 10 pixels
                        cv2.circle(merged_image, (int(x_intermediate), int(y_intermediate)), 10, (0, 255, 255), -1)

        # Affichage de l'image fusionnée
        merged_image = cv2.resize(merged_image, (800, 800))
        cv2.imshow('output_and_merged', np.hstack([output, merged_image]))
        cv2.waitKey(0)

    print("Liste des couleurs des cercles fusionnés:", merged_colors)
    print("Distances entre les points où les lignes sont tracées:", distances)
    print("Coordonnées des points utilisés pour les lignes tracées:", lines_info)
    return output, circle_count, merged, merged_colors

img = "plateauideal.jpg"
detect_circles(img)
