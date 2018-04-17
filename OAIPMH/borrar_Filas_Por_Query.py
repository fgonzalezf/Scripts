import arcpy, os,sys

tabla = sys.argv[1]
query=sys.argv[2]
#RECORD_ID in ( 'WELL_CSBE1006_COPIA1', 'WELL_CSBE1006_COPIA2')

arcpy.MakeTableView_management(tabla,"tablafiltro",query)

arcpy.DeleteRows_management("tablafiltro")

arcpy.Delete_management("tablafiltro")