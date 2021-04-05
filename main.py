# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PIL import Image
def GetNeighbors(point,r,cords):
    neighbors = []
    for x in range(-r,r):
        for y in range(-r,r):
            if(x*x + y*y <= r*r) and (point[0]+x,point[1]+y) in cords:
                neighbors.append((point[0]+x,point[1]+y))
    return neighbors
def GetNeighborsAverage(point,r,cords):
    neighbors = []
    pAmount = 0
    pXSum = 0
    pYSum = 0
    for x in range(-r,r):
        for y in range(-r,r):
            if(x*x + y*y <= r*r) and (point[0]+x,point[1]+y) in cords:
                neighbors.append((point[0]+x,point[1]+y))
                pAmount += 1
                pXSum += point[0] + x
                pYSum += point[1] + y
    return (round(pXSum/pAmount),round(pYSum/pAmount)),neighbors
def Generate_GCODE(x,y,z,speed):
    return f"G01 X{x} Y{y} F{speed}"
def ConvertPicToCords(image,thershold=50):
    image = image.convert('L')
    cords = []
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            if p <= thershold:
                cords.append((x,y))
    return cords
def CordsToGroups(cords):
    checked = []
    average_Points = []
    for cord in cords:
        if cord not in checked:
            aCord,neighbors = GetNeighborsAverage(cord, 4,cords)
            print(aCord)
            average_Points.append(aCord)
            checked.append(cord)
            checked.extend(neighbors)
    return average_Points,checked
def plot_points_on_img(points,img,color=(255,0,0)):
    for cord in points:
        img.putpixel(cord,color)
    return img



img = Image.open("A.png")
cords = ConvertPicToCords(img)
averages,checked = CordsToGroups(cords)
print(checked)
Average_img = plot_points_on_img(averages,img)
Average_img.show()
checked_img = plot_points_on_img(checked,img)
checked_img.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
