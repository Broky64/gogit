import numpy as np
import cv2 as cv
from scipy.spatial.distance import cdist
import math
import itertools
def points_equidistant(biggest, center_x,center_y):
    #d'abord il faut regroupé les points proches entre eux
    points_proches = []
    
    #print('biggest',biggest, 'area',max)
    list_indice=[]
    for i in range (len(biggest)):
        if i not in list_indice:
            list_médian=[]
            x1 ,y1 = biggest[i][0]
            #cv.circle(contour_img, (x1, y1), 15, (0, 255, 255), -1)
            list_médian.append([x1, y1])
            for j in range(i+1,len(biggest)):
                x2 ,y2 = biggest[j][0]
                distance = ((x2-x1)**2+(y2-y1)**2)**(1/2)
                if distance < 50:
                    list_indice.append(j)
                    list_médian.append([x2,y2])
            points_proches.append(list_médian)
    print('points_proches',points_proches)

    #puis trouver le points le plus proche du barycentre dans chaque groupe
    distance_centre=[]
    points_equidistant = []
    for elem in points_proches:
        x, y = elem[0]
        distance = ((center_x - x) ** 2 + (center_y - y) ** 2) ** (1 / 2)
        distance_centre.append(distance)
    for i in range (len(distance_centre)):
        eq_dist = [distance_centre[i]]
        index_coins=[i]
        for j in range (i+1,len(distance_centre)):
            if abs(distance_centre[i]-distance_centre[j])<30:
                eq_dist.append(distance_centre[j])
                index_coins.append(j)
            if len(eq_dist) == 4:
                for index in index_coins:
                    points_equidistant.append(points_proches[index])
    print('points_equidistant',points_equidistant)
    return points_equidistant
biggest =[[[ 96, 237]], [[429, 257]], [[149, 609]], [[680, 615]], [[668, 279]], [[684, 619]], [[145, 613]], [[180, 259]], [[418, 628]], [[127, 632]], [[698, 632]], [[418, 628]], [[647, 251]]]
# biggest= [[[ 96 237]]

#  [[429 257]]

#  [[149 609]]

#  [[680 615]]

#  [[668 279]]

#  [[684 619]]

#  [[145 613]]

#  [[180 259]]

#  [[418 628]]


#  [[698 632]]

#  [[418 628]]
#  [[647 251]]]


center_x=417
center_y=442
result=points_equidistant(biggest,417,442)