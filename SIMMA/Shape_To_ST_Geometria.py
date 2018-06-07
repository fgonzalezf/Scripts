import arcpy, os,sys

ShapeFile =r"C:\Users\Desarrollo\Documents\SIMMA\SHP_SIMMA_187\SHP_SIMMA_187\SHAPE_MM187_MAGNA.shp"

fields = ["@SHAPE","CodSimma"]


with arcpy.da.SearchCursor(ShapeFile, fields) as cursor:
        for row in cursor:
           print str(row[0])