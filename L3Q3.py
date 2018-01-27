'''
Finds all airports within 50km of AT RISK airports and marks them as MED RISK
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
def findHighRiskAirports(airports, roads) :
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


'''
First find all high risk airports
Select all airports with Security == AT RISK
Create a 50km buffer polygon around those airports
Select all airports within the polygon
For each airport in the selection:
    -If the airport is LOW RISK:
        -Change Security to MED RISK
'''
def findAirportRisks(airports, roads) :
    findHighRiskAirports(airports, roads)
    #SELECTBYLOCATION requires that airports be a feature layer
    arcpy.MakeFeatureLayer_management(airports, "atRisk_airports_lyr")
    selection = arcpy.SelectLayerByAttribute_management("atRisk_airports_lyr", "NEW_SELECTION", "Security='AT RISK'")
    medRiskArea = arcpy.Buffer_analysis(selection, "Buffered_At_Risk", "50000 meters", "FULL", "ROUND", "ALL")
    bufferedAtRisk = "Buffered_At_Risk.shp"
    selection = arcpy.SelectLayerByLocation_management("atRisk_airports_lyr", "WITHIN", medRiskArea, "", "", "")
    with arcpy.da.UpdateCursor(selection, "Security") as cursor:
            for row in cursor:
                if row[0] == "SAFE" :
                    row[0] = "MED RISK"
                    cursor.updateRow(row)

#Main                   
findAirportRisks(apt, rds)
