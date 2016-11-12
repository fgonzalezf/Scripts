import arcpy,os,sys

Geoadatabase = r"C:\Users\fernando.gonzalez\Documents\Integracion_25K\BK\fernandogonzalez_25K.sde"


def CalcularHoja(FeatuareClass,indice,Campo,Valor):
    try:
        arcpy.MakeFeatureLayer_management(indice,"LayerExtent",Campo+"='"+Valor+"'")
        arcpy.MakeFeatureLayer_management(FeatuareClass,"LayerCapa")
        arcpy.SelectLayerByLocation_management("LayerCapa","INTERSECT","LayerExtent","-2 METERS","NEW_SELECTION")
        result = arcpy.GetCount_management("LayerCapa")
        count=int(result.getOutput(0))
        if count>0:

            edit = arcpy.da.Editor(Geoadatabase)
            edit.startEditing(False, True)
            edit.startOperation()

            with arcpy.da.UpdateCursor("LayerCapa", "HOJA") as cursor:
                for row in cursor:
                    if row[0] is None:
                        row[0]=Valor
                        cursor.updateRow(row)

            edit.stopOperation()
            edit.stopEditing(True)
    except Exception as e:
        print "Error "+ e.message
    arcpy.Delete_management("LayerExtent")
    arcpy.Delete_management("LayerCapa")


def ListadoHojas(Indice,Feat):
    arcpy.MakeFeatureLayer_management(Indice,"LayerExtent")
    arcpy.MakeFeatureLayer_management(Feat,"LayerCapa")
    arcpy.SelectLayerByLocation_management("LayerExtent","INTERSECT","LayerCapa","","NEW_SELECTION")
    Listado=[]
    with arcpy.da.SearchCursor("LayerExtent", "HOJA") as cursor:
        for row in cursor:
            Listado.append(row[0])
    arcpy.Delete_management("LayerExtent")
    arcpy.Delete_management("LayerCapa")
    return Listado


arcpy.env.workspace= Geoadatabase

ListaDatasets=arcpy.ListDatasets("ADM25MIL*", "Feature")
Indice=r"C:\Users\fernando.gonzalez\Documents\Integracion_25K\BK2\Indice_Hoja_Cartografica.shp"
#Planchas=ListadoHojas(Indice)
FeatuaresConInformacion=[]
print "Recorriendo Geodatabase"
for dataset in ListaDatasets:
    arcpy.env.workspace=Geoadatabase+os.sep+dataset
    ListaFeatureClass= arcpy.ListFeatureClasses()
    for fc in ListaFeatureClass:
        result = arcpy.GetCount_management(fc)
        count=int(result.getOutput(0))
        desc= arcpy.Describe(fc)
        if  desc.featureType=="Annotation":
            print fc
            FeatuaresConInformacion.append(Geoadatabase+os.sep+dataset+os.sep+fc)
            print fc


NumeroCapas = len(FeatuaresConInformacion)
print "Numero de Capas "+str(NumeroCapas)
capaActual=0
for Feat in FeatuaresConInformacion:
    capaActual=capaActual+1
    planchaActual=0
    Planchas=ListadoHojas(Indice,Feat)
    NumeroPlanchas=len(Planchas)
    for plancha in Planchas:
        planchaActual=planchaActual+1
        print os.path.basename(Feat)
        print Feat+"...(" +str(capaActual)+  os.sep+str(NumeroCapas) + ")"  + "..."+ plancha + "...." + str(planchaActual)+" de "+str(NumeroPlanchas)
        CalcularHoja(Feat,Indice,"HOJA",plancha)
