import arcpy, os,sys

ExcelEntrada= sys.argv[1]
PesonalGeodatabase=sys.argv[2]
NombreSalida=sys.argv[3]

arcpy.env.overwriteOutput=True

Tabla=PesonalGeodatabase+os.sep+"TempTab"
arcpy.ExcelToTable_conversion(ExcelEntrada,Tabla)

#Crear Feature poligono

arcpy.env.workspace=Tabla
sr = arcpy.SpatialReference(4326)

Poligono = PesonalGeodatabase+os.sep+NombreSalida

arcpy.AddMessage(Poligono)
arcpy.CreateFeatureclass_management(PesonalGeodatabase,os.path.basename(Poligono),"POLYGON","","","",sr)
arcpy.AddField_management(Poligono,"ID_POLIGONO","LONG")


#Valores unicos "Lista"
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

ListaPoligonos =unique_values(Tabla,"ID_POLIGONO")
print ListaPoligonos
delimeter=arcpy.AddFieldDelimiters(PesonalGeodatabase+os.sep+"TempTab","ID_POLIGONO")
#print coordsList
fields=["No_VERTICE","X","Y"]
cur = None
try:
    for pol in ListaPoligonos:
        coordsList = arcpy.da.TableToNumPyArray(Tabla, fields, null_value=0,
                                                where_clause= delimeter+"="+str(pol))
        arcpy.AddMessage(delimeter+"="+str(pol))
        coordsList.sort()
        print coordsList
        cur = arcpy.da.InsertCursor(Poligono, ['SHAPE@','ID_POLIGONO'])

        array = arcpy.Array()
        ID = -1
        for coords in coordsList:
            print coords[0]
            if ID == -1:
                ID = pol

            if ID != pol:
                cur.insertRow([arcpy.Polygon(array,sr),ID])
                array.removeAll()
            array.add(arcpy.Point(float(coords[1]), float(coords[2])))
            ID = pol

        cur.insertRow([arcpy.Polygon(array,sr),ID])


except Exception as e:
   print arcpy.AddMessage(e.message)
finally:

    if cur:
        del cur

arcpy.Delete_management(Tabla)

