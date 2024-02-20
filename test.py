import cv2
import numpy as np

def detect_lines_and_stones(image_path):
    # Lire l'image
    img = cv2.imread(image_path)
    if img is None:
        print("Impossible de lire l'image. Veuillez vérifier le chemin.")
        return
    
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Appliquer la détection des bords de Canny
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Détecter les lignes à l'aide de la transformation de Hough
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    # Si des lignes sont détectées, afficher le nombre de lignes
    if lines is not None:
        print("Nombre de lignes détectées :", len(lines))
    else:
        print("Aucune ligne détectée.")

    # Détecter les cercles à l'aide de la transformation de Hough des cercles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

    # Si des cercles sont détectés, afficher le nombre de pierres
    if circles is not None:
        print("Nombre de pierres détectées :", len(circles[0]))
    else:
        print("Aucune pierre détectée.")

    # Afficher l'image avec les lignes détectées
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Afficher l'image avec les cercles détectés
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 4)

    # Afficher l'image résultante
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Appel de la fonction avec le chemin de l'image en argument
detect_lines_and_stones("3.jpg")
