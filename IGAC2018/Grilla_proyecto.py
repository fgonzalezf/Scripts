import arcpy,os,sys,random

PoligonoProyecto=r"C:\Users\Fernando\Downloads\INFORMACION PARA FERNANDO\INFORMACION PARA FERNANDO\GRILLAS\temp\Lim_Project.shp"
Escala="2000"
Muestra=30
CarpetaSalida=r"C:\Users\Fernando\Downloads\INFORMACION PARA FERNANDO\INFORMACION PARA FERNANDO\GRILLAS\temp"

EscalaMetros={"1000":50, "2000":100, "5000":250, "10000":500, "25000":1000}


def FindIdentificador(Feat):
    Identificador=""
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.type=="OID":
            Identificador=field.name
    return Identificador
def QueryPlancha (Feat):
    fields=['SHAPE@WKT',"SHAPE@"]
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
            print(int(round(row[1].extent.XMin)))
            print(int(round(row[1].extent.YMin)))
            print(int(round(row[1].extent.XMax)))
            print(int(round(row[1].extent.YMax)))
            print(row[1])

            return ([int(round(row[1].extent.XMin)),int(round(row[1].extent.YMin)),int(round(row[1].extent.XMax)),int(round(row[1].extent.YMax))])

def CreateFishnet(coordenadas, featOut, lonMarco):
    Largo = (coordenadas[2] - coordenadas[0])
    Alto = (coordenadas[3] - coordenadas[1])
    filas = int(round(Alto/lonMarco))
    columnas = int(round(Largo/lonMarco))
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

def SeleccionMuestra (capa,numeroMuestra, limiteProyecto):

    #crear Query
    salida=None
    arcpy.env.workspace=CarpetaSalida
    if CarpetaSalida in (".mdb") or CarpetaSalida in (".gdb"):
        outfc = arcpy.ValidateTableName("Grilla_aleatoria")
    else:
        outfc = arcpy.ValidateTableName("Grilla_aleatoria.shp")


    if limiteProyecto!="":
        salidainter=arcpy.MakeFeatureLayer_management(capa,"salida")
        salida = arcpy.SelectLayerByLocation_management(salidainter,"WITHIN_CLEMENTINI",limiteProyecto)
    else:
        salida=capa

    identificador = FindIdentificador(salida)
    fields = [identificador]
    Lista = []
    with arcpy.da.SearchCursor(salida, fields) as cursor:
        for row in cursor:
            Lista.append(row[0])
    random.shuffle(Lista)
    ListaAleatoria = Lista[:numeroMuestra]

    campo=arcpy.AddFieldDelimiters(salida,identificador)
    QueryAleatorio= campo+"in "+str(tuple(ListaAleatoria))
    arcpy.Select_analysis(salida,outfc ,QueryAleatorio)
Grilla=CarpetaSalida+os.sep+"Grilla_Completa.shp"
coord=QueryPlancha(PoligonoProyecto)
CreateFishnet(coord,Grilla,100)
SeleccionMuestra(Grilla,Muestra,PoligonoProyecto)