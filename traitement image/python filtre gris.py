from matplotlib import pyplot as plt
import matplotlib.image as mpimg

image=plt.imread("plateau idéal.png")
nb_ligne=image.shape[0]
nb_colonne=image.shape[1]
copie=image.copy()
for i in range(0,nb_ligne):
    for j in range(0,nb_colonne):
        gris=image[i][j][0]*0.299+image[i][j][1]*0.587+image[i][j][2]*0.114
        if gris<0.45:
            copie[i][j]=0
        else:
            copie[i][j]=1
plt.imshow(copie)
plt.show()
