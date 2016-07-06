__author__ = 'alberto'
import arcpy,os,sys

Geodatabase =r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\REPARADAS\File_Integrada_2014_v5_R.gdb"
Campo="INOBJECTID"


arcpy.env.workspace=Geodatabase
ListaDatasets=arcpy.ListDatasets()

for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase+os.sep+dataset
    listaFeat= arcpy.ListFeatureClasses()
    for fc in listaFeat:
        desc=arcpy.Describe(fc)
        if desc.featureType=="Annotation":
                print "Borrando" + fc
                try:
                    arcpy.DeleteField_management(fc,Campo)
                except:
                    pass
