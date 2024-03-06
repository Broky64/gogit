import datetime
from test import hough_transform

# Obtenir les informations sur les intersections à partir de hough_transform
intersection_info = hough_transform("4.jpg")

# Nom du fichier SGF à créer
sgf = "votre_nom_de_fichier.sgf"

# Taille du fichier SGF
size = 9

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
    if color== "noir": 
        color ="B"
    else :
     color="W"
    with open(file_name , "a") as file:
        file.write(f";{color}[{intersection}]\n")

# Créer le fichier SGF avec un nom spécifique et une taille
create_empty_file(sgf, size)

# Parcourir la liste intersection_info pour effectuer les mouvements dans le fichier SGF
for intersection in intersection_info:
    moove(sgf, intersection[2], intersection[1])

# Fermer le fichier SGF
with open(sgf, "a") as file:
    file.write(")")
