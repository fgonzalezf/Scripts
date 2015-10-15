import arcpy, os, sys

geodatabase = arcpy.GetParameterAsText(0)
txtsalida = arcpy.GetParameterAsText(1)
arcpy.env.workspace= geodatabase

datasets=arcpy.ListDatasets()

Fileprj = open (txtsalida, "w")

for dataset in datasets:
    arcpy.env.workspace=geodatabase+os.sep+dataset
    listfc = arcpy.ListFeatureClasses()
    for fc in listfc:
        Fileprj.write(fc + "\n")
Fileprj.close()
