import arcpy, os , sys

fields=[]
fc=[]

def mapeo(**campos):
    return campos

with arcpy.da.SearchCursor(fc, fields) as cursor:
    mapeoCampos = mapeo(
            FT_PLANCHA="Llave",
            PLANCHA="Campo1",
            FECHA_DILIGENCIAMIENTO="Campo2",
            ESCALA="Campo2",
            FECHA_RESTITUCION="Campo3")
    for row in cursor:
        print('{0}, {1}, {2}'.format(row[0], row[1], row[2]))
