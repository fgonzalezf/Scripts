import arcpy, os,sys
geodatabaseEntrada=r""

mapeoCampos={"Plancha":"plancha"}

with arcpy.da.SearchCursor(fc, fields) as cursor:
    for row in cursor:
        print(u'{0}, {1}, {2}'.format(row[0], row[1], row[2]))
