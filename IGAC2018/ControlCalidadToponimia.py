import arcpy, os,sys

GeodatabaseTopo=r"C:\Users\APN\Documents\IGAC\INFORMACION PARA FERNANDO\10000\172IIIA1\172IIIA1_Depurada.gdb"
GeodatabaseGeo=r"C:\Users\APN\Documents\IGAC\INFORMACION PARA FERNANDO\10000\172IIIA1_RS_2016_V1.mdb"

def CountMoreZero(Feat):
    X=0
    with arcpy.da.SearchCursor(Feat, "OBJECTID") as cursor:
        for row in cursor:
            if X>0:
                break
            X = X+1
    return X

def recorrerTopo(geodatabase):
    arcpy.env.workspace=geodatabase
    ListaFeat=arcpy.ListFeatureClasses()
    ListaCapasTopo=[]
    for fc in ListaFeat:
        count = CountMoreZero(fc)
        print fc + "..." + str(count)
        if count > 0:
            ListaCapasTopo.append(geodatabase+ os.sep+ fc)
    return ListaCapasTopo

def recorreGeo (geodatabase):
    arcpy.env.workspace = geodatabase
    ListaDatasets= arcpy.ListDatasets("*","Feature")
    ListaCapasGeo =[]
    for dataset in ListaDatasets:
        arcpy.env.workspace=geodatabase+os.sep+dataset
        listaCapas = arcpy.ListFeatureClasses()

        for fc in listaCapas:
            describefc= arcpy.Describe(fc)
            if describefc.featureType != "Annotation":
                count = CountMoreZero(fc)
                print fc +"..."+ str(count)
                if count > 0:
                    ListaCapasGeo.append(geodatabase+os.sep+dataset+os.sep+fc)
    return ListaCapasGeo

print recorrerTopo(GeodatabaseTopo)
print recorreGeo(GeodatabaseGeo)
