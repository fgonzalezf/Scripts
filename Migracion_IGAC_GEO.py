import arcpy, os, sys
GeodatabaseEntrada=r""
GeodatabaseSalida=r""

arcpy.env.workspace=GeodatabaseEntrada

for dataset in arcpy.ListDatasets("*","feature"):
    arcpy.env.workspace=GeodatabaseEntrada+os.sep+dataset
    for fc in arcpy.ListFeatureClasses():
        arcpy.env.workspace=GeodatabaseSalida+os.sep+"Mapa_Base"
        for feat in arcpy.ListFeatureClasses():
            if fc==feat:
                try:
                    arcpy.Append_management(fc,feat,"NO_TEST")
                except Exception as ex:
                    arcpy.AddMessage("Error Migrando..."+ fc +"..."+ex.message)