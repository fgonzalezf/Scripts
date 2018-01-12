import arcpy, os ,sys

capaEntrada =r""
capaInterseccion=r""

layerEntrada= arcpy.MakeFeatureLayer_management(capaEntrada,"layerEntrada")
layerInterseccion= arcpy.MakeFeatureLayer_management(capaInterseccion,"layerInterseccion")

arcpy.SelectLayerByLocation_management("layerEntrada",)