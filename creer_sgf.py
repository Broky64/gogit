import datetime

color = "W"
column= "a"
row = "a"

sgf = input("entrez le nom du fichier sgf \n")
size = 9
def create_empty_file(file_name, size):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    fichier = open(file_name , "w") 
    fichier.write("(;\n")
    fichier.write("FF[4]\n")
    fichier.write("CA[UTF-8]\n")
    fichier.write("GM[1]\n")
    fichier.write(f"DT[{date}]\n")
    fichier.write(f"SZ[{size}]\n")
    fichier.close()

create_empty_file(sgf, size)




create_empty_file(sgf, size)
