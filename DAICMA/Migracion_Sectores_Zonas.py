import arcpy,os,sys

arcpy.env.workspace = r"C:\Users\pache\Documents\Pruebas_Cargue\daicma2.gdb"

ListaFeatureClass= arcpy.ListFeatureClasses()

for fc in ListaFeatureClass:
    print fc