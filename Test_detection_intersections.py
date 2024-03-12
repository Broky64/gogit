import cv2
import numpy as np

def detect_circles(image_path): 
    img = cv2.imread(image_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 40, param1=90, param2=18, minRadius=15, maxRadius=24)
#1.15, 40, param1=60, param2=18, minRadius=8, maxRadius=15
    circle_count = 0  
    circle_centers = []  
    circle_colors = []  

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))

        for (x, y, r) in detected_circles[0, :]:

            roi = binary[y-r:y+r, x-r:x+r]
            mean_val = np.mean(roi)
            print (x,y,r,"roi :",mean_val)
            cv2.circle(output, (x, y), r, (0, 255, 0) if mean_val >= 50 else (255, 0, 0), 3)
            circle_centers.append((x, y, r))  
            circle_colors.append("blanc" if mean_val >= 50 else "noir")  
            circle_count += 1  
            cv2.circle(output, (x, y), 3, (255, 0, 0), -1)

        print("Coordonnées des centres des cercles détectés:", circle_centers)
        print("Nombre total de cercles détectés:", circle_count)

        while True:
            circles_merged = False  
            for i in range(len(circle_centers) - 1, 0, -1):
                for j in range(i - 1, -1, -1):  
                    x1, y1, r1 = circle_centers[i]
                    x2, y2, r2 = circle_centers[j]
                    dist_centers = np.sqrt((np.int64(x1) - np.int64(x2))**2 + (np.int64(y1) - np.int64(y2))**2)  
                    if dist_centers < 50:
                        print("distance entre les cercles : ", dist_centers, "cercles 1 :", circle_centers[i], "cercles 1 :", circle_centers[j])
                        print(f"Les centres des cercles {i+1} et {j+1} sont proches, fusion en cours...")
                        new_x = int((x1 + x2) / 2)
                        new_y = int((y1 + y2) / 2)
                        new_r = int((r1 + r2) / 2)
                        circle_centers.append((new_x, new_y, new_r))
                        roi = binary[new_y-new_r:new_y+new_r, new_x-new_r:new_x+new_r]
                        mean_val = np.mean(roi)
                        print(new_x,new_y,new_r,"roi :",mean_val)
                        circle_colors.append("blanc" if mean_val >= 50 else "noir")
                        print(f"Nouveau cercle à ({new_x}, {new_y}) avec un rayon de {new_r}")
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

        # Affichage des cercles avec les couleurs appropriées
        merged_image = img.copy()
        output = cv2.resize(output, (800, 800))

        for (x, y, r), color in zip(merged, merged_colors):
            if color == "blanc":
                cv2.circle(merged_image, (x, y), r, (0, 255, 0), 3)  # vert pour les cercles blancs
            else:
                cv2.circle(merged_image, (x, y), r, (255, 0, 0), 3)  # bleu pour les cercles noirs

            cv2.circle(merged_image, (x, y), 3, (255, 255, 255), -1)
            cv2.putText(merged_image, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # Affichage de l'image fusionnée
        merged_image = cv2.resize(merged_image, (800, 800))
        cv2.imshow('output_and_merged', np.hstack([output, merged_image]))
        cv2.waitKey(0)
    print("Liste des couleurs des cercles fusionnés:", merged_colors)
    return output, circle_count, merged, merged_colors

img = "plateauideal.jpg"
detect_circles(img)
