import cv2
import numpy as np

def hough_transform(image_path):
    # Lire l'image en niveaux de gris
    image = cv2.imread(image_path, 0)
    
    # Appliquer l'algorithme de Canny pour détecter les contours
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    
    # Appliquer la transformée de Hough pour détecter les lignes
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    
    # Initialiser le compteur d'intersections
    intersection_count = 0
    
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
                A = np.array([
                    [np.cos(theta1), np.sin(theta1)],
                    [np.cos(theta2), np.sin(theta2)]
                ])
                b = np.array([[rho1], [rho2]])
                intersection_point = np.linalg.solve(A, b)
                if (0 <= intersection_point[0] < image.shape[1]) and (0 <= intersection_point[1] < image.shape[0]):
                    intersection_count += 1
                    cv2.circle(image, (int(intersection_point[0]), int(intersection_point[1])), 5, (0, 255, 0), -1)
    
    # Afficher l'image avec les lignes et les intersections détectées
    cv2.imshow("Hough Lines and Intersections", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return intersection_count

# Chemin vers l'image à traiter
image_path = "coup1.png"

# Appel de la fonction pour détecter les lignes et compter les intersections
intersection_count = hough_transform(image_path)
print("Nombre d'intersections trouvées :", intersection_count)