import arcpy, os,sys

Grilla=r""
Plancha = ""

arcpy.env.workspace=Grilla

def unique_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

myValues = unique_values(Grilla,Plancha)
