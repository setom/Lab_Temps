'''
Finds all airports within 50km of AT RISK airports and marks them as MED RISK
'''

import arcpy
from arcpy import env
env.workspace = "D:\Projects\ArcGIS Projects\GIS501_Lab3\RAW_DATA\Exercise07"
#Overwrite files if they exist
arcpy.env.overwriteOutput = True 
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


'''
Create a new (empty) shp with 'name' param (fix naming convention if requ'd)
Select all airports with Security == AT RISK || Security == MED RISK
For each airport:
    insert them to the shp file
'''
def createAirportRiskShpOLD(name, airports) :
    name = name.replace(" ", "_")
    arcpy.CreateFeatureclass_management(env.workspace, name, "POINT", "", "", "",  arcpy.Describe(airports).spatialReference)
    arcpy.MakeFeatureLayer_management(airports, "atRisk_medRisk_airports_lyr")
    #add the fields to new shpfile
    fds = arcpy.ListFields(airports)
    selection = arcpy.SelectLayerByAttribute_management("atRisk_medRisk_airports_lyr", "NEW_SELECTION", "Security = 'AT RISK' OR Security = 'MED RISK'") 
    #TODO: CONTINUE BELOW - THIS ISN"T WORKING
    with arcpy.da.SearchCursor(selection, "*") as seCursor :
        for seRow in seCursor :
            with arcpy.da.InsertCursor(name, "*") as inCursor :
                inCursor.insertRow(seRow)
                    

'''
Fix the name of the output shp if required
Select all airports from the AT RISK or MED RISK
Copy those features to a new feature layer with the desired name
'''
def createAirportRiskShp(name, airports) :
    name = name.replace(" ", "_")
    arcpy.MakeFeatureLayer_management(airports, "atRisk_medRisk_airports_lyr")
    selection = arcpy.SelectLayerByAttribute_management("atRisk_medRisk_airports_lyr", "NEW_SELECTION", "Security = 'AT RISK' OR Security = 'MED RISK'") 
    arcpy.CopyFeatures_management(selection, name)

    
#********************** Main **************************
#Process the Airports shp to properly encode AT RISK, MED RISK and SAFE
findAirportRisks(apt, rds)
#Create the output shapefile
createAirportRiskShp("Alaska at risk.shp", apt)
