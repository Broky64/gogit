import datetime
from test import hough_transform
from ligne_colonne import goban

# Obtenir les informations sur les intersections à partir de hough_transform
img = "processed_image3.jpg"
# intersection_info = hough_transform(img)
_, intersection_info = goban(img)

# Nom du fichier SGF à créer
sgf = "oui.sgf"

# Taille du fichier SGF
size = 19

# Fonction pour créer un fichier SGF vide
def create_empty_file(file_name, size):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(file_name, "w") as file:
        file.write("(;\n")
        file.write("FF[4]\n")
        file.write("CA[UTF-8]\n")
        file.write("GM[1]\n")
        file.write(f"DT[{date}]\n")
        file.write(f"SZ[{size}]\n")

# Fonction pour effectuer un mouvement dans le fichier SGF
def moove(file_name, color, intersection):
    if color == "noir":
        color = "B"
    else:
        color = "W"
    with open(file_name, "a") as file:
        file.write(f";{color}[{intersection}]\n")

# Créer le fichier SGF avec un nom spécifique et une taille
create_empty_file(sgf, size)

# Charger les dernières informations sur les intersections
last_intersection_info = []

# Vérifier s'il y a de nouvelles coordonnées dans intersection_info
for coord_info in intersection_info:
    if coord_info not in last_intersection_info:
        moove(sgf, coord_info[2], coord_info[1])

# Mettre à jour last_intersection_info avec les nouvelles coordonnées détectées
last_intersection_info = intersection_info[:]

# Répéter le même processus pour une nouvelle image (processed_image4.jpg dans cet exemple)
img_new = "processed_image4.jpg"
_, intersection_info_new = goban(img_new)

# Vérifier s'il y a de nouvelles coordonnées dans intersection_info_new
for coord_info_new in intersection_info_new:
    if coord_info_new not in last_intersection_info:
        moove(sgf, coord_info_new[2], coord_info_new[1])

# Mettre à jour last_intersection_info avec les nouvelles coordonnées détectées
last_intersection_info = intersection_info_new[:]

# Fermer le fichier SGF
with open(sgf, "a") as file:
    file.write(")")
