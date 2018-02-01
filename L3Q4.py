import turtle
import arcpy
from arcpy import env
env.workspace = "D:\Projects\ArcGIS Projects\GIS501_Lab3\RAW_DATA\Exercise07"
#Overwrite files if they exist
arcpy.env.overwriteOutput = True 

'''
Returns the number of sides a user wants for a polygon
'''
def getSides() :
    sides = input("How many sides do you want the turtle to draw?")
    while sides < 3 :
        sides = input("Polygons must have at least 3 sides! How many sides do you want to draw?")
    return sides

'''
Param number of sided polygon to draw
Returns an arcpy array of points for X sided polygon
'''
def getArray(sides) :
    array = arcpy.Array()
    point = arcpy.Point()
    angle = (((sides - 2) * 180) / sides) - 180
    wn = turtle.Screen()
    turt = turtle.Turtle()
    while sides > 0:
        turt.left(angle)
        turt.forward(50)
        point.ID = sides
        point.X = turt.xcor()
        point.Y = turt.ycor()
        array.add(point)
        sides -= 1
    return array
    wn.exitonclick()

'''
Param arcpy array of points
Returns X
Creates a feature of given points
'''
def makePolygon(array) :
    sr = arcpy.SpatialReference(4326)
    arcpy.CreateFeatureclass_management(env.workspace, "turtle_polygon.shp", "POLYGON", "", "", "", sr)
    polygon = arcpy.Polygon(array)
    cursor = arcpy.da.InsertCursor("turtle_polygon.shp", ["SHAPE@"])
    cursor.insertRow([polygon])
    del cursor
    
#Main
sides = getSides()
array = getArray(sides)
makePolygon(array)

