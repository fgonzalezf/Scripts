#__author__ = 'fgonzalez'
import arcpy, os, sys
inFC = r"C:\temp\testLines.shp"
outFC = r"C:\temp\testLinesSplit.shp"
if arcpy.Exists(outFC):
    arcpy.Delete_management(outFC)
    arcpy.CreateFeatureclass_management("C:/temp","testLinesSplit.shp","POLYLINE","#","DISABLED","DISABLED",inFC)
    arcpy.AddField_management(outFC,"inFID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
iCursor = arcpy.da.InsertCursor(outFC, ["inFID","SHAPE@"])
with arcpy.da.SearchCursor(inFC,["OID@", "SHAPE@"]) as sCursor:
    for row in sCursor:
        inFID = row[0] # Print the current multipoint's ID
        # print("Feature {0}:".format(row[0]))
        partnum = 0 # Step through each part of the feature
        for part in row[1]: # Print the part number
            print("Part {0}:".format(partnum)) # Step through each vertex in the feature #
            prevX = None
            prevY = None
            for pnt in part:
                if pnt: # Print x,y coordinates of current point #
                    print("{0}, {1}".format(pnt.X, pnt.Y))
                    if prevX:
                        array = arcpy.Array([arcpy.Point(prevX, prevY), arcpy.Point(pnt.X, pnt.Y)])
                        polyline = arcpy.Polyline(array)
                        iCursor.insertRow([inFID,polyline])
                        prevX = pnt.X
                        prevY = pnt.Y
                    else: # If pnt is None, this represents an interior ring #
                        partnum += 1
del iCursor
arcpy.JoinField_management(outFC,"inFID",inFC,"FID","#")

arcpy.AddError("")

