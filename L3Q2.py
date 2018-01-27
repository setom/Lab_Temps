'''
Adds a 'Security' field to airports. Airports are 'at risk' if within 10000m of a road
all other airports are 'safe'
'''

import arcpy
from arcpy import env
env.workspace = "D:\Projects\ArcGIS Projects\GIS501_Lab3\RAW_DATA\Exercise07"
#Get the airport shapefile
apt = "airports.shp"
#Get the road shapefile
rds = "roads.shp"


'''
Add a Security field to the Airports Atribute table
Create a buffer polygon around the roads
Select airports that are within the buffer polygon
For each airport in the selection:
    - update the Security field to AT RISK
Invert the selection
For each airport in the selection:
    - update the Security field to SAFE
'''
def findAtRiskAirports(airports, roads) :
    arcpy.AddField_management(airports, "SECURITY", "TEXT", "", "", "25", "", "", "")
    riskArea = arcpy.Buffer_analysis(roads, "Buffered_Roads", "10000 meters", "FULL", "ROUND", "ALL")
    bufferedRoads = "Buffered_Roads.shp"
    #SELECTBYLOCATION requires that airports be a feature layer
    arcpy.MakeFeatureLayer_management(airports, "airports_lyr")
    selection = arcpy.SelectLayerByLocation_management("airports_lyr", "WITHIN", bufferedRoads, "", "", "")
    with arcpy.da.UpdateCursor(selection, "Security") as cursor:
            for row in cursor:
                    row[0] = "AT RISK"
                    cursor.updateRow(row)
    selection = arcpy.SelectLayerByLocation_management("airports_lyr", "WITHIN", bufferedRoads, "", "", "INVERT")
    with arcpy.da.UpdateCursor(selection, "Security") as cursor:
            for row in cursor:
                    row[0] = "SAFE"
                    cursor.updateRow(row)



#Main                   
findAtRiskAirports(apt, rds)
