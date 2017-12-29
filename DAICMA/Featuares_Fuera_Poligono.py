import arcpy, os, sys

DatasetEntrada= r"C:\Users\APN\Documents\GDB\Bk_GDB.gdb\DAICMA"
excelRuta=r"C:\Users\APN\Documents\GDB"

CapaColombia=DatasetEntrada+os.sep+"Colombia"
#LayerColombia=arcpy.MakeFeatureLayer_management(CapaColombia)

arcpy.env.workspace =DatasetEntrada


listaFeatures = arcpy.ListFeatureClasses()

for fc in listaFeatures:
    if fc != "Colombia":
        print fc
        layer = arcpy.MakeFeatureLayer_management(DatasetEntrada+os.sep+fc)
        arcpy.SelectLayerByLocation_management(layer,"INTERSECT",CapaColombia,"","NEW_SELECTION","INVERT")
        arcpy.TableToExcel_conversion(layer,excelRuta+os.sep+fc+"_Fuera.xls")

