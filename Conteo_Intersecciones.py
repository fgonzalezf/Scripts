import arcpy, os, uuid
#points = arcpy.GetParameterAsText(0)
polys = arcpy.GetParameterAsText(1)
buffer= arcpy.GetParameterAsText(2)
#points=r"D:\APN\Shapes_Villa_Hermosa\Shapes\EscuelasZona1.shp"
#polys=r"D:\APN\Shapes_Villa_Hermosa\Shapes\Sectores.shp"
#buffer="2 Meters"
CarpetaSalida =arcpy.GetParameterAsText(3)
arcpy.env.overwriteOutput=True
bufferDist=str(buffer)+ " Meters"
bufferPoint = "in_memory/points_Buffer"
arcpy.Buffer_analysis(points,bufferPoint,bufferDist)
Poligonos=arcpy.FeatureClassToFeatureClass_conversion(polys,CarpetaSalida,"Salida")
arcpy.AddField_management(Poligonos,"Conteo","LONG")
arcpy.MakeFeatureLayer_management(bufferPoint, "pointsLyr")

with arcpy.da.UpdateCursor(Poligonos, ["OID@", "SHAPE@","Conteo"]) as cursor:
    for row in cursor:
        arcpy.SelectLayerByLocation_management("pointsLyr", select_features = row[1])
        count = int(arcpy.GetCount_management("pointsLyr").getOutput(0))
        row[2]=count
        cursor.updateRow(row)

arcpy.Delete_management(bufferPoint)
arcpy.Delete_management("pointsLyr")
Poligonos=arcpy.SetParameterAsText(4,arcpy.FeatureSet(Poligonos))

