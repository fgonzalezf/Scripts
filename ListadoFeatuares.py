# -*- coding: utf-8 -*-
import arcpy, os, sys

#geodatabase = arcpy.GetParameterAsText(0)
geodatabase=sys.argv[1]
#txtsalida = arcpy.GetParameterAsText(1)
txtsalida=sys.argv[2]
arcpy.env.workspace= geodatabase

datasets=arcpy.ListDatasets()

Fileprj = open (txtsalida, "w")

for dataset in datasets:
    Fileprj.write(dataset.encode("utf-8") + " , " + "FeatureDataset" + "\n")
    arcpy.env.workspace=geodatabase+os.sep+dataset
    listfc = arcpy.ListFeatureClasses()
    for fc in listfc:
        arcpy.AddMessage(fc)
        Fileprj.write(fc.encode("utf-8") + " , " + "FeatureClass" + "\n")
        try:
            listfields = arcpy.ListFields(fc)
            for field in listfields:
                Fileprj.write(field.name.encode("utf-8") + " , " + field.type.encode("utf-8") +   "\n")
        except Exception as e:
            arcpy.AddMessage("Error..." + e.message)

arcpy.env.workspace= geodatabase
listFeatures = arcpy.ListFeatureClasses()
for fc in listFeatures:
    arcpy.AddMessage(fc)
    Fileprj.write(fc.encode("utf-8") + " , " + "FeatureClass" + "\n")
    try:
        listfields = arcpy.ListFields(fc)
        for field in listfields:
            Fileprj.write(field.name.encode("utf-8") + " , " + field.type.encode("utf-8") + "\n")
    except Exception as e:
        arcpy.AddMessage("Error..." + e.message)

arcpy.env.workspace= geodatabase
listtablas = arcpy.ListTables()
for tab in listtablas:
    arcpy.AddMessage(tab)
    Fileprj.write(tab.encode("utf-8") + " , " + "table" + "\n")
    try:
        listfields = arcpy.ListFields(tab)
        for field in listfields:
            Fileprj.write(field.name.encode("utf-8") + " , " + field.type.encode("utf-8") + "\n")
    except Exception as e:
        arcpy.AddMessage( "Error..." + e.message)

arcpy.env.workspace= geodatabase
listrasters = arcpy.ListRasters()
for ras in listrasters:
    arcpy.AddMessage(ras)
    Fileprj.write(ras.encode("utf-8") + " , " + "table" + "\n")
    try:
        listfields = arcpy.ListFields(ras)
        for field in listfields:
            Fileprj.write(field.name.encode("utf-8") + " , " + field.type.encode("utf-8") + "\n")
    except Exception as e:
        arcpy.AddMessage( "Error..." + e.message)

Fileprj.close()
