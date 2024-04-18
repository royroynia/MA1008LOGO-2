#initialise stage
import os
import math
import turtle

plist = []
vlist = []
blist = []
clist = []
coordlist = []
polygons = []

#functions color protection

def Colorprotection(colorfill):
    while True:
        safe_colors = ["red", "blue", "green", "yellow", "orange", "purple", "white", "black", "grey", "beige", "azure", "cyan", "lightgreen", "gold", "violet"]
        if colorfill.lower() in safe_colors:
            turtle.fillcolor(colorfill)
            break
        else:
            print("Error Unsafe color. Please Choose from: ", safe_colors)
            print()
            colorfill = input("Choose the color again: ")
#Rotation Matrix
def rotation_matrix(angle):
    rad = math.radians(angle)
    cos_theta = math.cos(rad)
    sin_theta = math.sin(rad)
    return [[cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]]

#translation matrix
def translation_matrix(tx, ty):
    return [[1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]]
#scale matrix
def scale_matrix(sx, sy):
    return [[sx, 0 , 0],
            [0, sy, 0],
            [0, 0 , 1]]
#skew matrix
def skew_matrix(sx, sy):
    return[[1, sx, 0],
           [sy, 1, 0],
           [0, 0, 1]]
#multiplying matrix
def matrix_multiply(mat, mat2):
    result = [[sum(a*b for a, b in zip(row, col)) for col in zip(*mat2)] for row in mat1]
    return result

#applying the transform
def apply_transform(matrix, coordinates):
    transformed_coords = []
    for x,y in coordinates:
        transformed = matrix_multiply(matrix, [[x], [y], [1]])
        transformed_coords.append((transformed[0][0], transformed[1][0]))
    return transformed_coords
#function to apply translation to the multiple polygons
def translate_polygons(polygons, tx, ty):
    translated_polygons = []
    translation_matrix = translation_matrix(tx, ty)
    for polygon in polygons:
        translated_polygon = apply_transform(translation_matrix, polygon)
        translated_polygons.append(translated_polygon)
    return translated_polygons

#functions to apply scaling to the polygons
def scale_polygons(polygons, sx, sy):
    scaled_polygons = []
    scaling_matrix = scaling_matrix(sx, sy)
    for polygon in polygons:
        scaled_polygon = apply_transform(scaling_matrix, polygon)
        scaled_polygons.append(scaled_polygon)
    return scaled_polygons

#functions to apply skewing to the polygons
def skew_polygons(polygons, sx, sy):
    skewed_polygons = []
    skewing_matrix = skew_matrix(sx, sy)
    for polygon in polygons:
        skewed_polygon = apply_transform(skewing_matrix, polygon)
        skewed_polygons.append(skewed_polygon)
    return skewed_polygons

#function to apply transformation to the polygons
def transform_polygons(polygons, translation, rotation_angle, scaling_factors, skew_factors):
    transformed_polygons = []
    translation_matrix = translation_matrix(*translation)
    rotation_matrix = rotation_matrix(rotation_angle)
    scaling_matrix = scaling_matrix(*scaling_factors)
    skew_matrix = skew_matrix(*skew_factors)

    combined_matrix = matrix_multiply(translation_matrix, rotation_matrix)
    combined_matrix = matrix_multiply(combined_matrix, scaling_matrix)
    combined_matrix = matrix_multiply(combined_matrix, skew_matrix)

    for polygon in polygons:
        transformed_polygon = apply_transform(combined_matrix, polygon)
        transformed_polygons.append(transformed_polygon)
    return transformed_polygons


#create function to ask for inputs defaults to 1 if no inputs
def userinputtss():
    while True:
        tx = float(input("Enter translation in x direction: "))
        ty = float(input("Enter translation in y direction: "))
        rotation_angle = float(input("Enter rotation angle (in degrees): "))
        sx = float(input("Enter scaling factor in x direction: "))
        sy = float(input("Enter scaling factor in y direction: "))
        sx2 = float(input("Enter skew factor in x direction: "))
        sy2 = float(input("Enter skew factor in y direction: "))

        return  tx, ty, sx, sy, sx2, sy2, rotation_angle

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Drawing functions

def drawLine(v1,v2,colorfill):
    turtle.color(colorfill)
    turtle.penup()
    turtle.speed(0)
    turtle.goto(v1)
    turtle.pendown()
    turtle.goto(v2)
    turtle.penup()

def drawBezierCurve (v1, v2, v3, v4,colorfill):
    for i in range(101):
        turtle.color(colorfill)
        t = i/100
        x = v1[0]*(1-t)**3 + 3*v2[0]*t*(1-t)**2 + 3*v3[0]*t*t*(1-t) + v4[0]*t**3
        y = v1[1]*(1-t)**3 + 3*v2[1]*t*(1-t)**2 + 3*v3[1]*t*t*(1-t) + v4[1]*t**3
        turtle.speed(0)
        turtle.goto(x, y)
        if i == 0: turtle.pendown()

def polygondraw (blist, vlist):
    a = 0
    while True:
        colorfill = input("Enter the colour for the polygon: ")
        Colorprotection(colorfill)
        turtle.begin_fill()
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(vlist[0]) #move the pen to the start of polygon coordinate
        while a < len(vlist):
            if a in blist:
                if a+1 == len(vlist):
                    drawBezierCurve(vlist[a], vlist[0], vlist[1], vlist[2],colorfill)
                    break
                else:
                    drawBezierCurve(vlist[a], vlist[a+1], vlist[a+2], vlist[a+3],colorfill)
                    a += 3 # move to the last vertex of the curve
            else:
                if a+1 == len(vlist):
                    drawLine(vlist[a], vlist[0],colorfill)
                    break
                else:
                    drawLine(vlist[a], vlist[a+1],colorfill)
                    a += 1 # move to the next vertex
        turtle.end_fill()
        break

#data parser
def parse_data(data):
    lines = data.split("\n")
    vlists = []
    blists = []
    bstack = []
    vstack = []
    is_polygon_data = False
    is_curve_data = False
    curve_count = 0
    for l in lines:
        # ignore empty lines
        if len(l) == 0:
            continue
        
        # ! indicate start of polygon
        if l.find('!') == 0:
            is_polygon_data = not is_polygon_data
            if is_polygon_data:
                if vstack or bstack:
                    # save polygon and reset stack
                    vlists.append(vstack)
                    blists.append(bstack)
                    vstack = []
                    bstack = []
            continue
        # # indicate the number of curves exists in the polygon
        elif l.find('#') == 0:
            is_curve_data = True
            curve_count = int(l.split(" ")[1])
            continue
        
        # if curve_count == 0 then just skip
        if curve_count == 0:
            is_curve_data = False

        if is_polygon_data:
            v1, v2 = l.split(" ")
            v1, v2 = float(v1), float(v2)
            vstack.append((v1,v2))
        elif is_curve_data:
            i = int(l)
            if i >= 0 and i < len(vstack):
                bstack.append(i)
            curve_count -= 1
    
    return blists, vlists


def draw(blists, vlists):
    for i in range(len(vlists)):
        polygondraw(blists[i], vlists[i])

#start of main program
prompt = 1


# drawing of the shapes (curves / straights)
while True:
    print("Choose how you would like to input your data:")
    print("1. Manually Key in each coordinates")
    print("2. Import data ")
    
    cond = input("Your selection: ")
    # Manually input data
    if cond == "2":
        while True:
            if __name__ == "__main__":
                filename = input("Enter the filename you wish to import: ")
                try:
                    with open(filename, "r") as f:
                        data = f.read()
                        blists, vlists = parse_data(data)
                        tx, ty, sx, sy, sx2, sy2, rotation_angle = userinputtss()
                        transformed_vlists = transform_polygons(vlists, (tx, ty), rotation_angle, (sx, sy), (sx2, sy2))
                        draw(blists, transformed_vlists)
                        turtle.hideturtle()
                        break
                except FileNotFoundError:
                    print()
                    print("Error, file not found, please ensure your file name is correct.")
                    print()
        while True:
            print("Choose one of the following options.")
            print("1. Choose another file.")
            print("2. Transform current file.")
            print("3. Accept current drawing.")
                
            neworend = input("Your selection: ")
            if neworend == "1":
                print()
            elif neworend == "2":
                break
            elif neworend == "3":
                turtle.stamp()
                turtle.hideturtle()
                break
            else:
                print("Error, please try again.")

            

    elif cond == "1":
        while True:
            
            #manually key in coordinates (from data set)
            numofpolygons = int(input("Enter the total number of polygons in the logo: "))

            for i in range (0, numofpolygons):
                print("Polygon number ", i+1)
                #ask for number of vertices
                numofvertices = int(input("Enter the number of vertices in the polygon: "))
                for i2 in range (0, numofvertices):
                    vertices = input("Enter the coordinate of the vertice (120 150): ")
                    if "abcdefghijklmnopqrstuvwxyz!,.@#$%&*()-=/?" in vertices:
                        print("Error, try again.")
                        i2 = i2-1
                    
                    else:
                        coordinates = vertices.split()
                        vlist.append([float(coordinates[0]), float(coordinates[1])])
                    
                while True:
                    qcurve = str(input("Is there any curves in the polygon to be drawn? (Y/N): "))
                    qcurve = qcurve.upper()
                    if qcurve == "Y":
                        numofcurves = int(input("How many curves are in the polygon?: "))
                        for i3 in range (0, numofcurves):
                            
                            startofcurve = int(input("Enter the vertex number that starts the curve [example: 4]: "))
                            blist.append(startofcurve)
                            
                        break
                    elif qcurve == "N":
                        break
                    else:
                        print("Invalid input try again.")
                polygondraw(blist, vlist)
                clist = vlist
                blist.clear()
                vlist.clear()
    #crash prevention        
    else:
        print()
        print("Input error, please try again.")
        print()
    
    while True:
        restartopt = input("Would you like to restart? (Y/N): ")
        restartopt = restartopt.upper()

        if restartopt == "Y":
            print()
            print("Program is restarting, clearing all data...")
            print()
        elif restartopt == "N":
            turtle.done()
            print()
            print("Thank you for using this program.")
            break

        else:
            print()
            print("Error, please try again.")
    break    
