import arcpy, os, uuid
#capaEstadisticas=r"C:\Users\Equipo\Documents\APN\Shapes\Sectores.shp"
#capaParametro=r"C:\Users\Equipo\Documents\APN\Shapes\EscuelasZona1.shp"
#campoEstadisticas="PK_CUE"
#Distancia="2 Kilometers"
#Clases=6

capaEstadisticas=arcpy.GetParameterAsText(0)
capaParametro=arcpy.GetParameterAsText(1)
campoEstadisticas=arcpy.GetParameterAsText(2)
Distancia=arcpy.GetParameterAsText(3)
Clases=arcpy.GetParameterAsText(4)

Carpeta =r"\\SRVAGSPRU\Temp"


arcpy.env.overwriteOutput=True


def normalizar(feat, field, Clases):
    values = [row[0] for row in arcpy.da.SearchCursor(feat, field)]
    Maximo = max(values)
    Minimo = min(values)
    # normalizar campo
    with arcpy.da.UpdateCursor(feat, field) as cursor:
        for row in cursor:
            try:
                valor = float(row[0])
                clasificacion = int((valor-Minimo)/(Maximo-Minimo)* int(Clases))
                row[0]= clasificacion
            except:
                row[0] = 0
            cursor.updateRow(row)


def mapeoCampos (Campo, Feat):
    CampoScope = arcpy.FieldMap()
    CampoScope.addInputField(Feat, Campo)
    Nombre = CampoScope.outputField
    Nombre.name=Campo
    CampoScope.outputField=Nombre
    fms = arcpy.FieldMappings()
    fms.addFieldMap(CampoScope)
    return fms

def CalculoScorpe(feat, fields):
    with arcpy.da.UpdateCursor(feat, fields) as cursor:
        for row in cursor:
            try:
                row[2] = row[0]*row[1]
            except:
                row[2] = 0
            cursor.updateRow(row)

    #Creacion de Layers

arcpy.MakeFeatureLayer_management(capaEstadisticas,"EstadisticasLyr")
arcpy.MakeFeatureLayer_management(capaParametro,"ParametroLyr")

#buffer en memoria
bufferParameter = "in_memory/parameter"
EstadisticasJoin = "in_memory/estadisticas"


arcpy.SelectLayerByLocation_management("ParametroLyr","INTERSECT","EstadisticasLyr",Distancia)

fieldMapping= mapeoCampos(campoEstadisticas,capaParametro)

arcpy.Buffer_analysis("ParametroLyr",bufferParameter,Distancia)
arcpy.SpatialJoin_analysis("EstadisticasLyr",bufferParameter,EstadisticasJoin,"JOIN_ONE_TO_ONE","KEEP_ALL",fieldMapping)

arcpy.AddField_management(EstadisticasJoin,"Scope","LONG")
#normalizar(EstadisticasJoin,campoEstadisticas)
fields= []
fields.append("Join_Count")
fields.append(campoEstadisticas)
fields.append("Scope")


CalculoScorpe(EstadisticasJoin,fields)
normalizar(EstadisticasJoin,"Scope",Clases)
nombreShape= "Salida.shp"
poligono= Carpeta+os.sep+nombreShape

if arcpy.Exists(poligono):
    arcpy.Delete_management(poligono)

arcpy.FeatureClassToFeatureClass_conversion(EstadisticasJoin,Carpeta,nombreShape)
arcpy.AddMessage(Carpeta+os.sep+nombreShape)


feature_set = arcpy.FeatureSet()
feature_set.load(poligono)
Poligonos=arcpy.SetParameterAsText(5,feature_set)
#arcpy.FeatureClassToFeatureClass_conversion(EstadisticasJoin,"C:\Users\Equipo\Documents\APN\Output","Salida")