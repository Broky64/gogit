import datetime

sgf = input("entrez le nom du fichier sgf que vous voulez créer\n ")
sgf += '.sgf'
size = 19
end = "n"
def create_empty_file(file_name, size): #file_name : nom du fichier que l'on veut créer, size : taille du plateau
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    file = open(file_name, "w") 
    file.write("(;\n")
    file.write("FF[4]\n")
    file.write("CA[UTF-8]\n")
    file.write("GM[1]\n")
    file.write(f"DT[{date}]\n")
    file.write(f"SZ[{size}]\n")
    file.close()

create_empty_file(sgf, size)

def moove(file_name, color, column, row) : #file_name : nom du fichier que l'on veut utiliser, color : couleur de la pierre, column : colonne sur laquelle se trouve la pierre, row : ligne sur laquelle se trouve la pierre
    file = open(file_name , "a")
    file.write(f";{color}[{column}{row}]\n")

while end != "y" :
    color = input("color")
    column= input("column")
    column = column.lower()
    row = input("row")
    row = row.lower()
    end = input("fin de partie ? (y or n)")
    moove(sgf, color, column, row)
    
file = open(sgf, "a")
file.write(")")