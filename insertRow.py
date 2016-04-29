__author__ = 'fernando.gonzalez'

import arcpy, os, sys

entrada=r'X:\PRUEBAS\Sandra_Gamba\Pruebas\prueba1\386ID.mdb\Relieve\Curva_Nivel'
salida=r'X:\PRUEBAS\Sandra_Gamba\Pruebas\prueba1\386IIC.mdb\Relieve\Curva_Nivel'
rows= arcpy.SearchCursor(entrada)
rows2=arcpy.InsertCursor(salida)
arcpy.gp.cr
for row in rows:
    rows2.insertRow(row)


del row
del rows
del rows2