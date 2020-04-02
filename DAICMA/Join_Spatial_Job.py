import arcpy, os,sys

FeatIn = r"C:\Users\APN\Downloads\GDB\BK_28_10_2019.gdb\DAICMA\Eventos"
FeatJoin = r"C:\Users\APN\Downloads\GDB\BK_28_10_2019.gdb\DAICMA\Municipios"
FeatOut=r"in_memory\Join_Feat"
FeatAppend= r"C:\Users\APN\Downloads\GDB\BK_28_10_2019.gdb\DAICMA\Eventos_Intervencion"

print "Iniciando Proceso"
arcpy.DeleteFeatures_management(FeatAppend)
arcpy.SpatialJoin_analysis(FeatIn , FeatJoin ,FeatOut,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
arcpy.Append_management(FeatOut,FeatAppend,"NO_TEST")

del FeatOut