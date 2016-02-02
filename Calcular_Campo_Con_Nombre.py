__author__ = 'fgonzalezf'

import arcpy,os, sys

carpeta =r"D:\Pruebas\AmenazaVolacnica\SPLIT"

arcpy.env.workspace=carpeta

for fc in arcpy.ListFeatureClasses():
    arcpy.AddMessage(fc)
    arcpy.AddField_management(fc,"COD_DANE","TEXT","","","40","COD_DANE")
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        row.setValue("COD_DANE", str(fc.replace(".shp","")))
        cursor.updateRow(row)


