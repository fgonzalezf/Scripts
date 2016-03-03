__author__ = 'alberto'
import arcpy,os,sys

Geodatabase =r"E:\IGAC\10K_V9.2_BOGOTA_CON_ANOTACIONES.mdb"
Carpetalayers=r"E:\IGAC\Layers"
Exportar="true"


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
                arcpy.env.workspace=Carpetalayers
                ListaLayers=arcpy.ListFiles()
                for layer in ListaLayers:
                    if fc+"Lyr"==layer[:-4]:
                        arcpy.DropRepresentation_cartography(fc,fc+"_Rep")
                        arcpy.AddRepresentation_cartography(fc,fc+"_Rep","RuleID","Override","STORE_CHANGE_AS_OVERRIDE",layer,"ASSIGN")




