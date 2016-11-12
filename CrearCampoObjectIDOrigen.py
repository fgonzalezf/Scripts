import arcpy, os, sys


Geodatabase=r"C:\Users\fernando.gonzalez\Documents\Integracion_25K\migracion_modelo_25k\Integrada_25_07_2016.gdb"
ListaLayers=arcpy.ListFiles()
arcpy.env.workspace=Geodatabase
ListaDatasets=arcpy.ListDatasets("*","Feature")



def CalculoID(Feat):
    fields = ['OID@', "OBJECT_ID_ORIGEN"]
    edit = arcpy.da.Editor(Geodatabase)
    edit.startEditing(False, True)
    edit.startOperation()
    with arcpy.da.UpdateCursor(Feat, fields) as cursor:
        for row in cursor:
            row[1]=row[0]
            cursor.updateRow(row)
    edit.stopOperation()
    edit.stopEditing(True)


for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase+os.sep+dataset
    listaFeat= arcpy.ListFeatureClasses()
    for fc in listaFeat:
        desc=arcpy.Describe(fc)
        if desc.featureType=="Annotation":
            print fc
            FeatureOrigen=Geodatabase+os.sep+dataset+os.sep+fc.replace("_Anot","")
            try:
                arcpy.AddField_management(FeatureOrigen,"OBJECT_ID_ORIGEN","LONG","","","","OBJECT_ID_ORIGEN")
            except Exception as e:
                print "error: "+e.message
            CalculoID(FeatureOrigen)