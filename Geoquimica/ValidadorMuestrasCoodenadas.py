import arcpy
arcpy.env.overwriteOutput=True

TablaGeografica= r"Database Connections\BDGQ.sde\BDGQ.SINSHAPE"
ConexionSDE=r"Database Connections\BDGQ.sde"
sr = arcpy.SpatialReference("WGS 1984")

layerSinBogota = arcpy.MakeQueryLayer_management(ConexionSDE,"layerSinBogota",
                                                    """SELECT *  FROM sinshape WHERE WGS84_LAT IS NULL AND (BOGOTA_ESTE IS NOT NULL AND BOGOTA_ORIGEN IS NOT NULL)"""
                                                    ,"OBJECTID","POINT","4326", sr)

layerSinMagna = arcpy.MakeQueryLayer_management(ConexionSDE,"layerSinMagna",
                                                    """SELECT *  FROM sinshape WHERE WGS84_LAT IS NULL AND (MAGNA_NORTE IS NOT NULL AND MAGNA_ORIGEN IS NOT NULL)"""
                                                    ,"OBJECTID","POINT","4326", sr)


#4326 WGS84

puntosLayer ="in_memory/puntos"
def ValoresEntrada(Feat,fields,CampoIdentificador):
    datos = {}
    tindx=0
    indx = 0
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[indx]] =row
    return datos

def Campos(Feat):
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    Lista.append('SHAPE@XY')
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name)
    return Lista

def indexUnico(CamposEntradaind,index):
    x=0
    for campo in CamposEntradaind:
        if campo == index:
            return x
        x=x+1

CampoUnico="ID_MUESTRA"

#arcpy.FeatureClassToFeatureClass_conversion(TablaGeografica,"in_memory","puntos")
arcpy.CreateFeatureclass_management("in_memory","puntos","POINT",layerSinBogota,"","",sr)

fieldsIn=Campos(layerSinBogota)
fieldsOut=Campos(puntosLayer)
print fieldsIn
print fieldsOut
cursor = arcpy.da.InsertCursor(puntosLayer,fieldsIn)



indxOut=indexUnico(fieldsIn,CampoUnico)
indxIn=indexUnico(fieldsIn,CampoUnico)
indxLogX=indexUnico(fieldsIn,"BOGOTA_ESTE")
indxLatY=indexUnico(fieldsIn,"BOGOTA_NORTE")
indxOrigen=indexUnico(fieldsIn,"BOGOTA_ORIGEN")
indxWGS84ELON=indexUnico(fieldsIn,"WGS84_LON")
indxWGS84NLAT=indexUnico(fieldsIn,"WGS84_LAT")

valoresEntradaBogota=ValoresEntrada(layerSinBogota,fieldsIn,CampoUnico)
count=len(valoresEntradaBogota)
valoresSalida=ValoresEntrada(puntosLayer,fieldsIn,CampoUnico)
Numerador=0
for keyvaluein in valoresEntradaBogota:
    Numerador = Numerador + 1

    if keyvaluein not in valoresSalida:
        try:
            print "Ingresando Valor..." + str(keyvaluein) + "....(" + str(Numerador) + " de " + str(count) + ")"
            rowin = valoresEntradaBogota[keyvaluein]
            rowin = list(rowin)
            pointBogota = arcpy.Point(rowin[indxLogX], rowin[indxLatY])
            origen = rowin[indxOrigen]
            pointWgs84=arcpy.PointGeometry(pointBogota, arcpy.SpatialReference(origen)).projectAs(arcpy.SpatialReference(4326))
            rowin[indxWGS84ELON]=pointWgs84.centroid.X
            rowin[indxWGS84NLAT] = pointWgs84.centroid.Y
            # del rowin[0]
            rowin.pop(0)
            rowin.insert(0, pointWgs84)
            rowin = tuple(rowin)
            # print rowin
            cursor.insertRow(rowin)
        except  Exception as e:

            print  "Error... " + e.message

indxOut=indexUnico(fieldsIn,CampoUnico)
indxIn=indexUnico(fieldsIn,CampoUnico)
indxLogX=indexUnico(fieldsIn,"MAGNA_ESTE")
indxLatY=indexUnico(fieldsIn,"MAGNA_NORTE")
indxOrigen=indexUnico(fieldsIn,"MAGNA_ORIGEN")
indxWGS84ELON=indexUnico(fieldsIn,"WGS84_LON")
indxWGS84NLAT=indexUnico(fieldsIn,"WGS84_LAT")
valoresEntradaBogota=ValoresEntrada(layerSinMagna,fieldsIn,CampoUnico)
count=len(valoresEntradaBogota)
valoresSalida=ValoresEntrada(puntosLayer,fieldsIn,CampoUnico)
Numerador=0
for keyvaluein in valoresEntradaBogota:
    Numerador = Numerador + 1

    if keyvaluein not in valoresSalida:
        try:
            print "Ingresando Valor..." + str(keyvaluein) + "....(" + str(Numerador) + " de " + str(count) + ")"
            rowin = valoresEntradaBogota[keyvaluein]
            rowin = list(rowin)
            pointBogota = arcpy.Point(rowin[indxLogX], rowin[indxLatY])
            origen = rowin[indxOrigen]
            pointWgs84=arcpy.PointGeometry(pointBogota, arcpy.SpatialReference(origen)).projectAs(arcpy.SpatialReference(4326))
            # del rowin[0]
            rowin[indxWGS84ELON] = pointWgs84.centroid.X
            rowin[indxWGS84NLAT] = pointWgs84.centroid.Y
            rowin.pop(0)
            rowin.insert(0, pointWgs84)
            rowin = tuple(rowin)
            # print rowin
            cursor.insertRow(rowin)
        except  Exception as e:

            print  "Error... " + e.message

#exportar temporal
arcpy.FeatureClassToFeatureClass_conversion(puntosLayer,r"C:\temp\Prueba1\Bk_04_22_2019.gdb","temp")