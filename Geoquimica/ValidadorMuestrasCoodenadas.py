import arcpy

TablaGeografica= r"Database Connections\BDGQ.sde\BDGQ.SINSHAPE"
ConexionSDE=r"Database Connections\BDGQ.sde"
sr = arcpy.SpatialReference("WGS 1984")

layerSinGeometria = arcpy.MakeQueryLayer_management(ConexionSDE,"SinGeometria",
                                                    """SELECT *  FROM sinshape WHERE WGS84_LAT IS NULL AND ((BOGOTA_ESTE IS NOT NULL AND BOGOTA_ORIGEN IS NOT NULL) OR (MAGNA_NORTE IS NOT NULL AND MAGNA_ORIGEN IS NOT NULL))"""
                                                    ,"OBJECTID","POINT","4326", sr)


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

arcpy.FeatureClassToFeatureClass_conversion(TablaGeografica,"in_memory","puntos")
cursor = arcpy.da.InsertCursor(puntosLayer, ["SHAPE@XY"])


print ValoresEntrada(layerSinGeometria,"*","OBJECTID")