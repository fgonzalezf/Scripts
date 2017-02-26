import arcpy, os,sys

ExcelEntrada= r"D:\APN\Excelpoligono\Poligono.xls"
PesonalGeodatabase=r"D:\APN\Excelpoligono\Prueba.mdb"

arcpy.env.overwriteOutput=True

Tabla=PesonalGeodatabase+os.sep+"TempTab"
arcpy.ExcelToTable_conversion(ExcelEntrada,Tabla)

#Crear Feature poligono

arcpy.env.workspace=Tabla
sr = arcpy.SpatialReference(4326)

arcpy.CreateFeatureclass_management(PesonalGeodatabase,"Poligono","POLYGON","","","",sr)
arcpy.AddField_management(PesonalGeodatabase+os.sep+"Poligono","ID_POLIGONO","LONG")
Poligono = PesonalGeodatabase+os.sep+"Poligono"
#Valores unicos "Lista"
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

ListaPoligonos =unique_values(Tabla,"ID_POLIGONO")
print ListaPoligonos

#print coordsList
fields=["No_VERTICE","X","Y"]
cur = None
try:
    for pol in ListaPoligonos:
        arcpy.AddFieldDelimiters()
        coordsList = arcpy.da.TableToNumPyArray(Tabla, fields, null_value=0,
                                                where_clause= """{0} = {1}""".format(arcpy.AddFieldDelimiters(PesonalGeodatabase, "ID_POLIGONO"),str(pol)))

        coordsList.sort()
        print coordsList
        cur = arcpy.da.InsertCursor(Poligono, ['SHAPE@','ID_POLIGONO'])

        # Create an array object needed to create features
        #
        array = arcpy.Array()

        # Initialize a variable for keeping track of a feature's ID.
        #
        ID = -1
        for coords in coordsList:
            print coords[0]
            if ID == -1:
                ID = pol

            # Add the point to the feature's array of points
            #   If the ID has changed, create a new feature
            #
            if ID != pol:
                cur.insertRow([arcpy.Polygon(array,sr),ID])
                array.removeAll()
            array.add(arcpy.Point(float(coords[1]), float(coords[2])))
            ID = pol

        # Add the last feature
        #
        cur.insertRow([arcpy.Polygon(array,sr),ID])


except Exception as e:
   print e.message
finally:
    # Cleanup the cursor if necessary
    #
    if cur:
        del cur
#leer tabla

