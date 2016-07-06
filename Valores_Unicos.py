__author__ = 'fgonzalezf'
import arcpy, os,sys

Entrada=r"D:\Pruebas\Municipios\Tabla.gdb\tabla"
Salida=r"D:\Pruebas\Municipios\Tabla.gdb\union"

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


ValoresUnicos = unique_values(Entrada, "Dane")
cursor2 = arcpy.da.InsertCursor(Salida,("DANE", "PLANCHAS"))


for valor in ValoresUnicos:
    with arcpy.da.SearchCursor(Entrada, ("Dane", "NUMERO_PLANCHA")) as cursor:
        print valor
        Y=""
        for row in cursor:
            if row[0]==valor:
                Y=Y+","+str(row[1])
        cursor2.insertRow((valor,Y))






