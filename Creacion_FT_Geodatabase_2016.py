import arcpy,os,sys

Geodatabase = r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\V10.1\TEMP\25K_con anotaciones\25K_10_02_2016_GEODATABASE_CARGUE.mdb"
CarpetaLayers= r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\10K_Gobernacion\GEODATABASE_VECTORES\CON_ANOTACIONES\FT_LAYERS"
def CreacionFT(Nombre,Ruta):

    Feat=arcpy.CreateFeatureclass_management(Ruta,Nombre,"POLYGON","","","ENABLED","")
    arcpy.AddField_management(Feat,"FT_PLANCHA","TEXT","","","20","","","","")
    arcpy.AddField_management(Feat,"PKCUE_ORIGEN","DOUBLE","","","","","","","")
    arcpy.AddField_management(Feat,"CAMBIO","TEXT","","","2","","","","Dom_Cambios")
    arcpy.AddField_management(Feat,"RESPONSABLE","TEXT","","","100","","","","")
    arcpy.AddField_management(Feat,"RESPONSABLE_CONTROL","TEXT","","","100","","","","")
    arcpy.AddField_management(Feat,"VIGENCIA","TEXT","","","2","","","","Dom_Vigencia")
    arcpy.AddField_management(Feat,"FECHA_MODIFICACION","DATE","","","","","","","")
    arcpy.AddField_management(Feat,"OBSERVACIONES","TEXT","","","255","","","","")
    return Feat



arcpy.env.workspace = CarpetaLayers
listaLayers=arcpy.ListFiles("*.lyr")

arcpy.env.workspace = Geodatabase
ListaDatasets= arcpy.ListDatasets()

for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase+os.sep+dataset
    ListaFeatuare = arcpy.ListFeatureClasses("FT_*")
    for fc in ListaFeatuare:
        print "Borrando: "+ fc
        Nombre = str(fc)
        arcpy.Delete_management(fc)
        print "Creando: "+ Nombre
        Nuevo=CreacionFT(Nombre,Geodatabase+os.sep+dataset)
        print "Creando Representacion"
        for layer in listaLayers:
            if layer[:-7]==Nombre:
                arcpy.AddRepresentation_cartography(Nuevo,arcpy.Describe(Nuevo.getOutput(0)).name+"_Rep","RuleID","Override","STORE_CHANGE_AS_OVERRIDE",CarpetaLayers+os.sep+layer,"NO_ASSIGN")







