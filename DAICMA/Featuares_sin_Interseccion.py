import arcpy, os ,sys

capaEntrada =r"D:\APN\mapasss\Scripts\GDB\Bk_GDB.gdb\DAICMA\Areas_Canceladas"
capaInterseccion=r"D:\APN\mapasss\Scripts\GDB\Bk_GDB.gdb\DAICMA\Area_Peligrosa"
excelSalida=r"D:\APN\mapasss\Scripts\GDB\Excel_Areas_Peligrosas_sin_Areas_Canceladas.xls"

layerEntrada= arcpy.MakeFeatureLayer_management(capaEntrada,"layerEntrada")
layerInterseccion= arcpy.MakeFeatureLayer_management(capaInterseccion,"layerInterseccion")

arcpy.SelectLayerByLocation_management("layerEntrada","INTERSECT","layerInterseccion","","","INVERT")

arcpy.TableToExcel_conversion("layerEntrada",excelSalida)

arcpy.Delete_management("layerEntrada")
arcpy.Delete_management("layerInterseccion")