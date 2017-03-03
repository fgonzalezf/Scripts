__author__ = 'fgonzalezf'
import arcpy, os ,sys

Featentrada=r""
FeatSalida=r""
Campo="Vereda"
suma=""

with arcpy.da.SearchCursor(Featentrada, (Campo)) as cursor:
    for row in cursor:
        suma = suma + " - " + str(row[0])
arcpy.Dissolve_management(Featentrada,FeatSalida)
arcpy.AddField_management(FeatSalida,Campo,"TEXT","","","255",Campo)
with arcpy.da.UpdateCursor(FeatSalida, Campo) as cursor:
    for row in cursor:
        row[0] = suma
        cursor.updateRow(row)
