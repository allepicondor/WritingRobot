# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
import numpy as np

def GetNeighbors(point, r, cords):
    neighbors = []
    for x in range(-r, r):
        for y in range(-r, r):
            if (x * x + y * y <= r * r) and (point[0] + x, point[1] + y) in cords:
                neighbors.append((point[0] + x, point[1] + y))
    return neighbors


def GetNeighborsAverage(point, r, cords):
    neighbors = []
    pAmount = 0
    pXSum = 0
    pYSum = 0
    for x in range(-r, r):
        for y in range(-r, r):
            if (x * x + y * y <= r * r) and (point[0] + x, point[1] + y) in cords:
                neighbors.append((point[0] + x, point[1] + y))
                pAmount += 1
                pXSum += point[0] + x
                pYSum += point[1] + y
    return (round(pXSum / pAmount), round(pYSum / pAmount)), neighbors


def Generate_GCODE(x, y, z, speed):
    return f"G01 X{x} Y{y} F{speed}"


def ConvertPicToCords(image, thershold=90):
    image = image.convert('L')
    cords = []
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            if p <= thershold:
                cords.append((x, y))
    return cords


def CordsToGroups(cords,radius=4):
    checked = []
    average_Points = []
    for cord in cords:
        if cord not in checked:
            aCord, neighbors = GetNeighborsAverage(cord, radius, cords)
            print(aCord)
            average_Points.append(aCord)
            checked.append(cord)
            checked.extend(neighbors)
    groups = []
    checked = []
    for point in average_Points:
        if point in checked :
            continue
        print(average_Points.index(point))
        Cgroup = []
        checked.append(point)
        for other in average_Points:
            if point != other:
                y1 = point[1]
                y2 = other[1]
                x1 = point[0]
                x2 = other[0]
                try:
                    m = (y2 - y1) / (x2 - x1)
                except ZeroDivisionError as e:
                    m = (y2 - y1)
                b = y1 - (m * x1)
                good = True
                for i in range(1, abs(x2 - x1)):
                    sY = m * (x1 + i) + b
                    if not (x1 + i, round(sY)) in cords:
                        good = False
                        break
                for i in range(1, abs(y2 - y1)):
                    sX = ((y1+i)-b)/m
                    if not (round(sX),y1 + i) in cords:
                        good = False
                        break
                if good:
                    Cgroup.append(other)
        groups.append(Cgroup)
        checked.extend(Cgroup)

    print("done")
    return average_Points, groups


def plot_points_on_img(points, nimg, color=(255, 0, 0)):
    img = nimg.copy()
    for cord in points:
        img.putpixel(cord, color)
    return img


img = Image.open("A.png")
cords = ConvertPicToCords(img)
print(cords)
averages, groups = CordsToGroups(cords,radius=2)
print(len(groups))
viewable_img = plot_points_on_img(groups[0], img, color=(255,0,0))
for group in groups:
    color = tuple(np.random.choice(range(0,256), size=3))
    viewable_img = plot_points_on_img(group, viewable_img, color=color)
    plot_points_on_img(group, img, color=color).show()
plot_points_on_img(averages, img, color=(255,0,0)).show()

viewable_img.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
