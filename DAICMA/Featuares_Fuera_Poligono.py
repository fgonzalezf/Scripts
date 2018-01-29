import arcpy, os, sys

DatasetEntrada= r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB\Bk_GDB.gdb\DAICMA"
excelRuta=r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB"

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


