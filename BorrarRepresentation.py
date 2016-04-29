__author__ = 'alberto'
import arcpy,os,sys

Geodatabase =r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.3_08_04_2016\25K\25K_08_04_2016_GEODATABASE_CARGUE.mdb"
Carpetalayers=r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.2_17_12_2016\proyectadas\25k_Sin_anotaciones\layers"
Exportar="false"

arcpy.env.workspace=Carpetalayers
ListaLayers=arcpy.ListFiles()
arcpy.env.workspace=Geodatabase
ListaDatasets=arcpy.ListDatasets()

for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase+os.sep+dataset
    listaFeat= arcpy.ListFeatureClasses()
    for fc in listaFeat:
        desc=arcpy.Describe(fc)
        if desc.featureType!="Annotation":
            if Exportar=="true":
                print "Exportando" + fc
                Layer=arcpy.MakeFeatureLayer_management(fc,fc+"Lyr")
                try:
                    arcpy.SetLayerRepresentation_cartography(fc+"Lyr",fc+"_Rep")
                except:
                    pass
                arcpy.SaveToLayerFile_management(fc+"Lyr",Carpetalayers+os.sep+fc+"Lyr")
                arcpy.Delete_management(Layer)
            else:

                for layer in ListaLayers:
                    if fc+"Lyr"==layer[:-4]:
                        print layer
                        try:
                            arcpy.DropRepresentation_cartography(Geodatabase+os.sep+dataset+os.sep+fc,fc+"_Rep")
                        except Exception as ex:
                            print "Error "+ ex.message
                        try:
                            arcpy.AddRepresentation_cartography(Geodatabase+os.sep+dataset+os.sep+fc,fc+"_Rep","RuleID","Override","STORE_CHANGE_AS_OVERRIDE",Carpetalayers+os.sep+layer,"ASSIGN")
                        except Exception as ex:
                            print "Error "+ ex.message