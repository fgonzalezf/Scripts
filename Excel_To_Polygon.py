import arcpy, os,sys

#ExcelEntrada= sys.argv[1]
#PesonalGeodatabase=sys.argv[2]
#NombreSalida=sys.argv[3]
ExcelEntrada= r"C:\Users\fgonzalezf\Documents\APN\Poligonos\Poligono.xls"
PesonalGeodatabase=r"C:\Users\fgonzalezf\Documents\APN\Poligonos\PoligonosSal.mdb"
NombreSalida="prueba4"
FeatSalida=r"C:\Users\fgonzalezf\Documents\APN\Poligonos\PoligonosSal.mdb\prueba3_1"
arcpy.env.overwriteOutput=True

#Valores unicos "Lista"
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

def ListFields (Tabla):
    ListFieldsIn=arcpy.ListFields(Tabla)
    ListaFinal =[]
    for field in ListFieldsIn:
        if field.name!="OBJECTID":
            ListaFinal.append(field.name)
    return ListaFinal

def updateFeat(Entrada, Salida, uniqueField):
    listaEntrada=unique_values(Entrada, uniqueField)
    listaSalida=unique_values(Salida, uniqueField)
    camposentradaConj = set(listaEntrada)
    camposSalidaConj = set(listaSalida)
    diferentes = camposentradaConj - camposSalidaConj
    normalizado = list(diferentes)
    if len(normalizado)>0:
        campo = arcpy.AddFieldDelimiters(Entrada, uniqueField)
        QueryCargar = campo + " in " + str(tuple(normalizado)).replace("u'","'")
        print QueryCargar
        arcpy.MakeFeatureLayer_management(Entrada,"Cargar",QueryCargar)
        arcpy.Append_management("Cargar",Salida,"NO_TEST")





Tabla=PesonalGeodatabase+os.sep+"TempTab"
arcpy.ExcelToTable_conversion(ExcelEntrada,Tabla,"Poligono")

#Crear Feature poligono

arcpy.env.workspace=Tabla
sr = arcpy.SpatialReference(4326)

Poligono = PesonalGeodatabase+os.sep+NombreSalida
fieldsTable = ListFields(Tabla)
fieldsPoligono =["SHAPE@"]
arcpy.CreateFeatureclass_management(PesonalGeodatabase,os.path.basename(Poligono),"POLYGON","","","",sr)
arcpy.AddMessage(fieldsTable)
for fieldname in fieldsTable:
    if fieldname!="No_VERTICE" and fieldname!="Y" and fieldname!="X":
        arcpy.AddField_management(Poligono,fieldname,"TEXT","","","255")
        fieldsPoligono.append(fieldname)
arcpy.AddMessage(fieldsPoligono)
ListaPoligonos =unique_values(Tabla,"ID_POLIGONO")
print ListaPoligonos
delimeter=arcpy.AddFieldDelimiters(PesonalGeodatabase+os.sep+"TempTab","ID_POLIGONO")
#print coordsList
fields=fieldsTable
cur = None
try:
    for pol in ListaPoligonos:
            coordsList = arcpy.da.TableToNumPyArray(Tabla, fields, null_value=0,where_clause= delimeter+"="+str(pol))
            arcpy.AddMessage(delimeter+"="+str(pol))
            coordsList.sort()
            cur = arcpy.da.InsertCursor(Poligono, fieldsPoligono)
            array = arcpy.Array()
            ID = -1
            for coords in coordsList:
                arcpy.AddMessage(coords)
                row=[]
                if ID == -1:
                    ID = pol
                if ID != pol:
                    row.append(arcpy.Polygon(array,sr))
                    row.append(coords[0])
                    for i in range(len(fields)):
                        if i>3:
                            row.append(coords[i])
                    array.removeAll()
                array.add(arcpy.Point(float(coords[2]), float(coords[3])))
                ID = pol
            row.append(arcpy.Polygon(array,sr))
            row.append(coords[0])
            for i in range(len(fields)):
                        if i>3:
                            row.append(coords[i])
            arcpy.AddMessage(len(row))
            cur.insertRow(row)
except Exception as e:
   arcpy.AddMessage("Error en el proceso..."+ e.message)
if cur:
    del cur

arcpy.Delete_management(Tabla)

updateFeat(PesonalGeodatabase+os.sep+NombreSalida,FeatSalida,"ID_POLIGONO")

