import cv2
import numpy as np

def detect_circles(image_path): 
    img = cv2.imread(image_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=60)

    circle_count = 0  # Compteur de cercles détectés

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))
        centers_list = []  # Liste pour stocker les coordonnées des centres des cercles détectés
        for (x, y, r) in detected_circles[0, :]:
            cv2.circle(output, (x, y), r, (0, 255, 0), 3)
            # Ajoute les coordonnées du centre et du rayon à la liste
            centers_list.append((x, y, r))  
            circle_count += 1  # Incrémente le compteur de cercles

        print("Coordonnées des centres des cercles détectés:", centers_list)
        print("Nombre total de cercles détectés:", circle_count)
        merged = centers_list.copy()
        # Boucle de fusion des cercles jusqu'à ce qu'aucune paire ne soit suffisamment proche
        while True:
            circles_merged = False  # Indique si des cercles ont été fusionnés lors de cette itération
            for i in range(len(centers_list),0,-1):
                for j in range(len(centers_list) - 1, i, -1):  # Utiliser une boucle en sens inverse
                    x1, y1, r1 = centers_list[i]
                    x2, y2, r2 = centers_list[j]
                    dist_centers = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)  
                    if dist_centers < 50:
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
                        # Afficher les nouvelles coordonnées
                        print(f"Nouveau cercle à ({new_x}, {new_y}) avec un rayon de {new_r}")
                        # Supprimer les cercles fusionnés de la liste
                        del centers_list[j]
                        del centers_list[i]
                        # Mettre à jour le compteur de cercles
                        circle_count -= 1
                        circles_merged = True
                        break  # Sortir de la boucle interne après la fusion
                if circles_merged:
                    break  # Sortir de la boucle externe si des cercles ont été fusionnés

            if not circles_merged:
                break  # Sortir de la boucle externe si aucune fusion n'a eu lieu

        print("Nombre de cercles après fusion:", circle_count)
        merged = centers_list.copy()
        print("nouveaux cercles",merged)
        
        # Dessiner les cercles après fusion
        for (x, y, r) in centers_list:
            cv2.circle(output, (x, y), r, (0, 0, 255), 3)
            # Ajouter les coordonnées du centre comme texte sur l'image
            cv2.putText(output, f"({x}, {y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Afficher l'image avec les cercles et les coordonnées
        output = cv2.resize(output, (700, 700))
        cv2.imshow('output', output)
        cv2.waitKey(0)

    return output, circle_count

img ="5.jpg"
detect_circles(img)
