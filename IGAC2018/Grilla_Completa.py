import arcpy, os, sys, random

Grilla=r"C:\Users\Fernando\Downloads\INFORMACION PARA FERNANDO\INFORMACION PARA FERNANDO\GRILLAS\2K\cuadr_bta.shp"
Muetra=20
CarpetaSalida=r"C:\temp"
LimiteProyecto=r"C:\Users\Fernando\Downloads\INFORMACION PARA FERNANDO\INFORMACION PARA FERNANDO\GRILLAS\temp\Lim.shp"
ExportarDGN="false"

def FindIdentificador(Feat):
    Identificador=""
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.type=="OID":
            Identificador=field.name
    return Identificador


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
        salida = arcpy.SelectLayerByLocation_management(salidainter,"INTERSECT",limiteProyecto,"-10 METERS")
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

def exportarDGN(CapaEntrada,capasalida):
    pathArcgis = os.environ["AGSDESKTOPJAVA"]
    arcpy.ExportCAD_conversion(CapaEntrada,"DGN_V8",capasalida,"","",pathArcgis+os.sep+"ArcToolbox/Templates/template3d.dgn")

try:
    SeleccionMuestra(Grilla,Muetra,LimiteProyecto)
except Exception as e:
    arcpy.AddError(e.message)
try:
    exportarDGN(Grilla, CarpetaSalida+os.sep+"Grilla_Aleatoria.dgn")