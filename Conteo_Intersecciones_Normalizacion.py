import arcpy, os, uuid
#capaEstadisticas=r"C:\Users\Equipo\Documents\APN\Shapes\Sectores.shp"
#capaParametro=r"C:\Users\Equipo\Documents\APN\Shapes\EscuelasZona1.shp"
#campoEstadisticas="PK_CUE"
#Distancia="2 Kilometers"

#Clases= 3 por Defecto

capaEstadisticas=arcpy.GetParameterAsText(0)
capaParametro=arcpy.GetParameterAsText(1)
campoEstadisticas=arcpy.GetParameterAsText(2)
Distancia=arcpy.GetParameterAsText(3)
#Clases=arcpy.GetParameterAsText(4)

Carpeta =r'D:\APN\Priorizacion\Geoprocesos'
arcpy.env.overwriteOutput=True

def normalizar(feat, field , fieldSal):
    values = [row[0] for row in arcpy.da.SearchCursor(feat, field)]
    Maximo = max(values)
    Minimo = min(values)
    if Minimo == None:
        Minimo =0
    arcpy.AddMessage("Maximo: "+str(Maximo))
    arcpy.AddMessage("Minimo: "+str(Minimo))
    # normalizar campo
    fieldsSal=[]
    fieldsSal.append(field)
    fieldsSal.append(fieldSal)
    with arcpy.da.UpdateCursor(feat, fieldsSal) as cursor:
        for row in cursor:
            try:
                valor = float(row[0])
                clasificacion = float((valor-Minimo)/(Maximo-Minimo))
                row[1]= clasificacion
            except:
                row[1] = 0
            cursor.updateRow(row)
def normalizarClases(feat, field ):
    values = [row[0] for row in arcpy.da.SearchCursor(feat, field)]
    Maximo = max(values)
    Minimo = min(values)
    if Minimo == None:
        Minimo =0
    arcpy.AddMessage("Maximo: "+str(Maximo))
    arcpy.AddMessage("Minimo: "+str(Minimo))
    # normalizar campo
    with arcpy.da.UpdateCursor(feat, field) as cursor:
        for row in cursor:
            try:
                valor = float(row[0])
                clasificacion = int(float((valor-Minimo)/(Maximo-Minimo))*3)
                if clasificacion ==3:
                    clasificacion = 2
                row[0] = clasificacion
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
    if len(fields)==3:
        with arcpy.da.UpdateCursor(feat, fields) as cursor:
            for row in cursor:
                try:
                    row[2] = row[0]+row[1]
                except:
                    row[2] = 0
                cursor.updateRow(row)
    else:
        with arcpy.da.UpdateCursor(feat, fields) as cursor:
            for row in cursor:
                try:
                    row[1] = row[0]
                except:
                    row[1] = 0
                cursor.updateRow(row)

def borrarTemporales():
    arcpy.env.workspace = Carpeta
    featureclasses = arcpy.ListFeatureClasses()
    for fc in featureclasses:
        try:
            arcpy.Delete_management(fc)
        except:
            pass

borrarTemporales()

arcpy.MakeFeatureLayer_management(capaEstadisticas,"EstadisticasLyr")
arcpy.MakeFeatureLayer_management(capaParametro,"ParametroLyr")

#buffer en memoria
bufferParameter = "in_memory/parameter"
nombreEstadisticas = "Estadisticas_"+str(uuid.uuid4()).replace("-","")[:10]+".shp"
estadisticas = Carpeta+ os.sep+ nombreEstadisticas
EstadisticasJoin = "in_memory/estadisticasJoin"

arcpy.FeatureClassToFeatureClass_conversion(capaEstadisticas,Carpeta,nombreEstadisticas)

arcpy.SelectLayerByLocation_management("ParametroLyr","INTERSECT","EstadisticasLyr",Distancia)
if campoEstadisticas != "":
    fieldMapping= mapeoCampos(campoEstadisticas,capaParametro)
else:
    fieldMapping = arcpy.FieldMappings()

arcpy.Buffer_analysis("ParametroLyr",bufferParameter,Distancia)
arcpy.SpatialJoin_analysis(estadisticas,bufferParameter,EstadisticasJoin,"JOIN_ONE_TO_ONE","KEEP_ALL",fieldMapping)
if campoEstadisticas != "":
    arcpy.AddField_management(EstadisticasJoin,"INDICADOR1","DOUBLE")
arcpy.AddField_management(EstadisticasJoin,"INDESPACIAL","DOUBLE")
arcpy.AddField_management(EstadisticasJoin,"CLASES","DOUBLE")

#normalizar(EstadisticasJoin,campoEstadisticas)

fields= []


normalizar(EstadisticasJoin,"Join_Count","INDESPACIAL")
if campoEstadisticas != "":
    normalizar(EstadisticasJoin,campoEstadisticas,"INDICADOR1")
fields.append("INDESPACIAL")
if campoEstadisticas != "":
    fields.append("INDICADOR1")
fields.append("CLASES")

CalculoScorpe(EstadisticasJoin,fields)

normalizarClases(EstadisticasJoin,"CLASES")

nombreShape= "Salida_"+str(uuid.uuid4()).replace("-","")[:10]+".shp"
poligono= Carpeta+os.sep+nombreShape

arcpy.FeatureClassToFeatureClass_conversion(EstadisticasJoin,Carpeta,nombreShape)
arcpy.AddMessage(Carpeta+os.sep+nombreShape)

#feature_set = arcpy.FeatureSet()
#feature_set.load(poligono)
arcpy.SetParameterAsText(4,arcpy.FeatureSet(poligono))

#arcpy.FeatureClassToFeatureClass_conversion(EstadisticasJoin,"C:\Users\Equipo\Documents\APN\Output","Salida")