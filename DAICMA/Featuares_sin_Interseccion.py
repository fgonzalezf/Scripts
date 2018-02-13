import arcpy, os ,sys

capaEntrada =sys.argv[1]
capaInterseccion=sys.argv[2]
excelSalida=sys.argv[3]

layerEntrada= arcpy.MakeFeatureLayer_management(capaEntrada,"layerEntrada")
layerInterseccion= arcpy.MakeFeatureLayer_management(capaInterseccion,"layerInterseccion")

arcpy.SelectLayerByLocation_management("layerEntrada","INTERSECT","layerInterseccion","","","INVERT")

arcpy.TableToExcel_conversion("layerEntrada",excelSalida)

arcpy.Delete_management("layerEntrada")
arcpy.Delete_management("layerInterseccion")