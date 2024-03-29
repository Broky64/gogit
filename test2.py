import cv2
import numpy as np

def find_nearest_intersection(circle_center, intersections):
    min_distance = float('inf')
    nearest_intersection = None

    for intersection in intersections:
        distance = np.sqrt((circle_center[0] - intersection[0]) ** 2 + (circle_center[1] - intersection[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_intersection = intersection

    return nearest_intersection

def label_intersections(intersections):
    labels_dict = {}
    label_index = 0
    for i in range(19):
        for j in range(19):
            if label_index < len(intersections):
                label = chr(97 + j) + chr(97 + i)
                labels_dict[label] = intersections[label_index]
                label_index += 1
    return labels_dict

def sort_intersections(intersections):
    return sorted(intersections, key=lambda x: (round(x[1]/14)*14, round(x[0])))

def hough_transform(image_path):
    original_image = cv2.imread(image_path)
    edges = cv2.Canny(original_image, 50, 200, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 250)

    intersection_count = 0
    intersections = []

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
            cv2.line(original_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                rho1, theta1 = lines[i][0]
                rho2, theta2 = lines[j][0]
                denominator = np.sin(theta1 - theta2)
                if denominator != 0:
                    A = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
                    b = np.array([[rho1], [rho2]])
                    intersection_point = np.linalg.solve(A, b)
                    if (0 <= intersection_point[0, 0] < original_image.shape[1]) and (0 <= intersection_point[1, 0] < original_image.shape[0]):
                        intersections.append((intersection_point[0, 0], intersection_point[1, 0]))
                        cv2.circle(original_image, (int(intersection_point[0, 0]), int(intersection_point[1, 0])), 5, (0, 255, 0), -1)

    intersections_merge = []
    i = 0
    while i < len(intersections):
        x1, y1 = intersections[i]
        x1, y1 = int(x1), int(y1)
        j = i + 1
        while j < len(intersections):
            x2, y2 = intersections[j]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if distance < 40:
                x1 = int((x1 + x2) / 2)
                y1 = int((y1 + y2) / 2)
                del intersections[j]
            else:
                j += 1
        intersections_merge.append((x1, y1))
        i += 1

    intersection_count = len(intersections_merge)
    intersections_merge = sort_intersections(intersections_merge)

    intersections_labeled = label_intersections(intersections_merge)
    print("Intersections étiquetées :")
    print(intersections_labeled)

    print("nombre d'intersections :", intersection_count)

    for x, y in intersections_merge:
        cv2.circle(original_image, (int(x), int(y)), 5, (0, 255, 0), -1)

    intersections_image = np.zeros_like(original_image)
    for x, y in intersections_merge:
        cv2.circle(intersections_image, (int(x), int(y)), 5, (0, 255, 0), -1)

    cv2.imshow('Intersections détectées', np.hstack((cv2.resize(original_image, (400, 400)), cv2.resize(intersections_image, (400, 400)))))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Exemple d'utilisation :
hough_transform("reflet.jpg")
