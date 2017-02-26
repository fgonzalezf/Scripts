import arcpy, os,sys

ExcelEntrada= r"C:\Users\Equipo\Documents\APN\Poligono.xls"
PesonalGeodatabase=r"C:\Users\Equipo\Documents\APN\Prueba.mdb"

Tabla=PesonalGeodatabase+os.sep+"TempTab"
arcpy.ExcelToTable_conversion(ExcelEntrada,Tabla)


arcpy.env.workspace=Tabla

#leer tabla
