import cv2
import numpy as np

def detect_contours(image_path):
    # Lire l'image en niveaux de gris
    image = cv2.imread(image_path, 0)
    
    # Appliquer l'algorithme de Canny pour détecter les contours
    edges = cv2.Canny(image, 400, 500)  # Les valeurs 100 et 200 sont des seuils pour la détection des contours

    # Afficher l'image originale et les contours détectés
    cv2.imshow("Detected Edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return intersection_count

# Chemin vers l'image à traiter
image_path = "coup1.png"

# Appel de la fonction pour détecter les contours
detect_contours(image_path)


