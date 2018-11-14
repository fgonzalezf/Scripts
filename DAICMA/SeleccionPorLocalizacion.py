import arcpy, os,sys

poligonoSeleccion=sys.argv[1]
datasetEntrada=sys.argv[2]
carpetaSalida=sys.argv[3]

arcpy.env.workspace=datasetEntrada
listaFeat= arcpy.ListFeatureClasses()

for fc in listaFeat:
    arcpy.AddMessage(fc)
    LayerSeleccion = arcpy.MakeFeatureLayer_management(fc, "layerSeleccion")
    seleccion = arcpy.SelectLayerByLocation_management(LayerSeleccion,"INTERSECT",poligonoSeleccion,"-10 Meters")
    result = arcpy.GetCount_management(seleccion)
    count = int(result.getOutput(0))
    if count>0:
        arcpy.FeatureClassToFeatureClass_conversion(seleccion,carpetaSalida,fc+".shp")
    arcpy.Delete_management(LayerSeleccion)


