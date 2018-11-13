import arcpy, os,sys,random


#Planchas=r"C:\Users\APN\Documents\IGAC\Planchas_10K_Planas\central.shp"
#campo=r""
#plancha="8IIIB1"
#CarpetaSalida=r"C:\temp"
#Escala=10000
Planchas=sys.argv[1]
campo=sys.argv[2]
plancha=sys.argv[3]
CarpetaSalida=sys.argv[4]
Escala=int(sys.argv[5])



NumeroMuestra=20
Filas=10
Columnas=15
arcpy.env.overwriteOutput=True

def CrearSalida(ruta,nombre):
    sptref=arcpy.Describe(Planchas)
    stref=sptref.spatialreference
    return arcpy.CreateFeatureclass_management(ruta,nombre,"POLYGON","","","",stref)

def FindIdentificador(Feat):
    Identificador=""
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.type=="OID":
            Identificador=field.name
    return Identificador
def QueryPlancha (Feat, plancha, campo):
    fields=['SHAPE@WKT',campo,"SHAPE@"]
    with arcpy.da.SearchCursor(Feat, fields, campo+"""="""+"'"+plancha+"'") as cursor:
        for row in cursor:
            print(int(round(row[2].extent.XMin)))
            print(int(round(row[2].extent.YMin)))
            print(int(round(row[2].extent.XMax)))
            print(int(round(row[2].extent.YMax)))
            print(row[2])

            return ([int(round(row[2].extent.XMin)),int(round(row[2].extent.YMin)),int(round(row[2].extent.XMax)),int(round(row[2].extent.YMax))])

def CreateFishnet(coordenadas, featOut, filas, columnas):
    Largo = (coordenadas[2] - coordenadas[0])
    Alto = (coordenadas[3] - coordenadas[1])
    LargoFish = (coordenadas[2]-coordenadas[0])/columnas
    AltoFish =(coordenadas[3]-coordenadas[1])/filas
    features = []
    for i in range(filas):
        YminFish=coordenadas[1]+(AltoFish*i)
        YmaxFish = coordenadas[1] + AltoFish+ (AltoFish*i)
        for j in range(columnas):
            XminFish = coordenadas[0] + (LargoFish * j)
            XmaxFish = coordenadas[0] + LargoFish+ (LargoFish * j)
            features.append(arcpy.Polygon
                            (arcpy.Array([
                                            arcpy.Point(XminFish,YminFish),
                                            arcpy.Point(XmaxFish,YminFish),
                                            arcpy.Point(XmaxFish,YmaxFish),
                                            arcpy.Point(XminFish,YmaxFish)])))
    arcpy.CopyFeatures_management(features, featOut)

def SeleccionMuestra (capa,numeroMuestra):
    identificador= FindIdentificador(capa)
    fields=[identificador]
    Lista=[]
    outfc=None
    arcpy.env.workspace = CarpetaSalida
    if CarpetaSalida in (".mdb") or CarpetaSalida in (".gdb"):
        outfc = arcpy.ValidateTableName("Grilla_aleatoria")
    else:
        outfc = arcpy.ValidateTableName("Grilla_aleatoria.shp")
    with arcpy.da.SearchCursor(capa, fields) as cursor:
        for row in cursor:
            Lista.append(row[0])
    random.shuffle(Lista)
    ListaAleatoria=Lista[:numeroMuestra]
    #crear Query
    campo=arcpy.AddFieldDelimiters(capa,identificador)
    QueryAleatorio= campo+"in "+str(tuple(ListaAleatoria))
    arcpy.Select_analysis(capa,outfc,QueryAleatorio)
    

Grilla=CrearSalida(CarpetaSalida,"Grilla2.shp")
coord=QueryPlancha(Planchas,plancha, campo)
CreateFishnet(coord,Grilla,Filas,Columnas)

SeleccionMuestra(Grilla,NumeroMuestra)