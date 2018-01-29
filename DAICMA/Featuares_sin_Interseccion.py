import arcpy, os ,sys

capaEntrada =r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB\Bk_GDB.gdb\DAICMA\Areas_Despejadas"
capaInterseccion=r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB\Bk_GDB.gdb\DAICMA\Area_Peligrosa"
excelSalida=r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB\Excel_Areas_Despejadas_Sin_Areas_Peligrosas.xls"

layerEntrada= arcpy.MakeFeatureLayer_management(capaEntrada,"layerEntrada")
layerInterseccion= arcpy.MakeFeatureLayer_management(capaInterseccion,"layerInterseccion")

arcpy.SelectLayerByLocation_management("layerEntrada","INTERSECT","layerInterseccion","","","INVERT")

arcpy.TableToExcel_conversion("layerEntrada",excelSalida)

arcpy.Delete_management("layerEntrada")
arcpy.Delete_management("layerInterseccion")