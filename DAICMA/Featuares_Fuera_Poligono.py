import arcpy, os, sys

DatasetEntrada= sys.argv[1]
excelRuta=sys.argv[2]

CapaColombia=DatasetEntrada+os.sep+"Colombia"
#LayerColombia=arcpy.MakeFeatureLayer_management(CapaColombia)

arcpy.env.workspace =DatasetEntrada


listaFeatures = arcpy.ListFeatureClasses()

for fc in listaFeatures:
    if fc != "Colombia":
        arcpy.AddMessage(fc)
        layer = arcpy.MakeFeatureLayer_management(DatasetEntrada+os.sep+fc)
        arcpy.SelectLayerByLocation_management(layer,"INTERSECT",CapaColombia,"","NEW_SELECTION","INVERT")
        arcpy.TableToExcel_conversion(layer,excelRuta+os.sep+fc+"_Fuera.xls")


