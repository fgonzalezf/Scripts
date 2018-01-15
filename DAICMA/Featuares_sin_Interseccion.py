import arcpy, os ,sys

capaEntrada =r"C:\Users\APN\Documents\APN\GDB\Bk_GDB.gdb\DAICMA\Areas_Canceladas"
capaInterseccion=r"C:\Users\APN\Documents\APN\GDB\Bk_GDB.gdb\DAICMA\Area_Peligrosa"
excelSalida=r"C:\Users\APN\Documents\APN\GDB\Excel_Areas_Canceladas_Sin_Areas_Peligrosas.xls"

layerEntrada= arcpy.MakeFeatureLayer_management(capaEntrada,"layerEntrada")
layerInterseccion= arcpy.MakeFeatureLayer_management(capaInterseccion,"layerInterseccion")

arcpy.SelectLayerByLocation_management("layerEntrada","INTERSECT","layerInterseccion","","","INVERT")

arcpy.TableToExcel_conversion("layerEntrada",excelSalida)

arcpy.Delete_management("layerEntrada")
arcpy.Delete_management("layerInterseccion")