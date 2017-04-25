import arcpy, os

points = arcpy.GetParameterAsText(0)
polys = arcpy.GetParameterAsText(1)
buffer= arcpy.GetParameterAsText(2)

arcpy.env.overwriteOutput=True

bufferDist=str(buffer)+ " Meters"
arcpy.Buffer_analysis(points,"in_memory/points_Buffer",bufferDist)

arcpy.MakeFeatureLayer_management("in_memory/points_Buffer", "pointsLyr")

data = {}
text_file = open(r"C:\temp\Output2.txt", "w")
with arcpy.da.SearchCursor(polys, ["OID@", "SHAPE@"]) as cursor:
    for row in cursor:
        arcpy.SelectLayerByLocation_management("pointsLyr", select_features = row[1])
        count = int(arcpy.GetCount_management("pointsLyr").getOutput(0))
        data[row[0]] = count
        text_file.write(str(row[0])+ "..."+ str(count) +"\n")
text_file.close()
arcpy.Delete_management("in_memory/points_Buffer")

arcpy.SetParameterAsText(3)