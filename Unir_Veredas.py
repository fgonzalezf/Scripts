__author__ = 'fernando.gonzalez'
import arcpy, os, sys
reload(sys)
sys.setdefaultencoding("utf-8")

tablaEntrada=sys.argv[1]
tablaSalida = sys.argv[2]
Campo_Union = sys.argv[3]


rows = arcpy.SearchCursor(tablaEntrada)
arcpy.Dissolve_management(tablaEntrada,tablaSalida)
arcpy.AddField_management(tablaSalida,Campo_Union,"TEXT","","","255",Campo_Union)

union=""
for row in rows:
    union = union + "_"+ row.getValue (Campo_Union)
rows2=arcpy.UpdateCursor(tablaSalida)
arcpy.AddMessage(union)
for row2 in rows2:
    row2.setValue(Campo_Union, union)
    rows2.updateRow(row2)

