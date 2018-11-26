import arcpy, os, sys, random

#Grilla=r"C:\Users\Fernando\Downloads\INFORMACION PARA FERNANDO\INFORMACION PARA FERNANDO\GRILLAS\2K\cuadr_bta.shp"
#Muetra=20
#CarpetaSalida=r"C:\temp"
#LimiteProyecto=r"C:\Users\Fernando\Downloads\INFORMACION PARA FERNANDO\INFORMACION PARA FERNANDO\GRILLAS\temp\Lim.shp"
#ExportarDGN="false"

Grilla=sys.argv[1]
Muetra=int(sys.argv[2])
CarpetaSalida=sys.argv[3]
LimiteProyecto=sys.argv[4]
boolExportarDGN=sys.argv[5]

arcpy.env.overwriteOutput=True

def FindIdentificador(Feat):
    Identificador=""
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.type=="OID":
            Identificador=field.name
    return Identificador


def SeleccionMuestra (capa,numeroMuestra, limiteProyecto):
    arcpy.env.workspace = Grilla
    sptref = arcpy.Describe(Grilla)
    stref = sptref.spatialreference
    arcpy.env.outputCoordinateSystem = stref
    #crear Query
    salida=None
    arcpy.env.workspace=CarpetaSalida
    if CarpetaSalida in (".mdb") or CarpetaSalida in (".gdb"):
        outfc = "Grilla_aleatoria"
    else:
        outfc = "Grilla_aleatoria.shp"


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

    campo=arcpy.AddFieldDelimiters(capa,identificador)
    QueryAleatorio= campo+"in "+str(tuple(ListaAleatoria))
    arcpy.Select_analysis(salida,outfc ,QueryAleatorio)
    if boolExportarDGN == "true":
        CapaAleatoria = CarpetaSalida + os.sep +  "Grilla_aleatoria.dgn"
        exportarDGN(outfc, CapaAleatoria)

def exportarDGN(CapaEntrada,capasalida):
    pathArcgis = os.environ["AGSDESKTOPJAVA"]
    arcpy.ExportCAD_conversion(CapaEntrada,"DGN_V8",capasalida,"","",pathArcgis+os.sep+"ArcToolbox/Templates/template3d.dgn")

try:
    SeleccionMuestra(Grilla,Muetra,LimiteProyecto)
except Exception as e:
    arcpy.AddError(e.message)
