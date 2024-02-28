import cv2
import numpy as np

def detect_circles(image_path): 
    img = cv2.imread(image_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=47)

    circle_count = 0  

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))
        centers_list = []  

        for (x, y, r) in detected_circles[0, :]:
            
            roi = binary[y-r:y+r, x-r:x+r]
            mean_val = np.mean(roi)

            cv2.circle(output, (x, y), r, (0, 255, 0) if mean_val > 127 else (255, 0, 0), 3)

            centers_list.append((x, y, r))  
            circle_count += 1  

            cv2.circle(output, (x, y), 3, (255, 0, 0), -1)

        print("Coordonnées des centres des cercles détectés:", centers_list)
        print("Nombre total de cercles détectés:", circle_count)

        while True:
            circles_merged = False  # Indique si des cercles ont été fusionnés lors de cette itération
            for i in range(len(centers_list), 0, -1):
                for j in range(len(centers_list) - 1, i, -1):  
                    x1, y1, r1 = centers_list[i]
                    x2, y2, r2 = centers_list[j]
                    dist_centers = np.sqrt((np.int64(x1) - np.int64(x2))**2 + (np.int64(y1) - np.int64(y2))**2)  
                    if dist_centers < 50:
                        print("distance entre les cercles : ", dist_centers, "cercles 1 :", centers_list[i], "cercles 1 :", centers_list[j])
                        print(f"Les centres des cercles {i+1} et {j+1} sont proches, fusion en cours...")
                        # Calculer le nouveau centre comme le milieu des deux cercles
                        new_x = int((x1 + x2) / 2)
                        new_y = int((y1 + y2) / 2)
                        # Calculer le nouveau rayon comme la moyenne des rayons des deux cercles
                        new_r = int((r1 + r2) / 2)
                        # Ajouter le nouveau cercle fusionné à la liste
                        centers_list.append((new_x, new_y, new_r))
                        # Marquer le nouveau cercle sur l'image
                        cv2.circle(output, (new_x, new_y), new_r, (255, 0, 0), 3)
                        # Dessiner un point de couleur au centre du nouveau cercle fusionné
                        cv2.circle(output, (new_x, new_y), 3, (255, 0, 0), -1)
                        # Afficher les nouvelles coordonnées
                        print(f"Nouveau cercle à ({new_x}, {new_y}) avec un rayon de {new_r}")
                        # Supprimer les cercles fusionnés de la liste
                        del centers_list[j]
                        del centers_list[i]
                        # Mettre à jour le compteur de cercles
                        circle_count -= 1
                        circles_merged = True
                        break  
                if circles_merged:
                    break  

            if not circles_merged:
                break  # Sortir de la boucle externe si aucune fusion n'a eu lieu

        print("Nombre de cercles après fusion:", circle_count)
        merged = centers_list.copy()
        print("nouveaux cercles", merged)

        # Partie détection de couleur
        circle_brightness = []  # Liste pour stocker la luminosité des cercles
        for (x, y, r) in merged:

            roi = binary[y-r:y+r, x-r:x+r]
            mean_val = np.mean(roi)

            if mean_val > 65:
                circle_brightness.append("blanc")
            else:
                circle_brightness.append("noir")

        print("Luminosité des cercles fusionnés:", circle_brightness)

        # Créez une copie de l'image d'origine
        merged_image = img.copy()

        # Dessinez les cercles fusionnés sur l'image fusionnée avec les coordonnées du centre
        for (x, y, r) in merged:
            color = (0, 255, 0) if circle_brightness[merged.index((x, y, r))] == "blanc" else (255, 0, 0)
            cv2.circle(merged_image, (x, y), r, color, 3)
            # Dessiner un point de couleur au centre du cercle fusionné
            cv2.circle(merged_image, (x, y), 3, color, -1)
            # Ajouter le texte avec les coordonnées du centre
            cv2.putText(merged_image, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # Affichez les deux images côte à côte
        output = cv2.resize(output, (800, 800))
        merged_image = cv2.resize(merged_image, (800, 800))
        cv2.imshow('output_and_merged', np.hstack([output, merged_image]))
        cv2.waitKey(0)

    return output, circle_count, merged

img = "bordel.jpg"
detect_circles(img)
