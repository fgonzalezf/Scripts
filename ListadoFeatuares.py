# -*- coding: utf-8 -*-
import arcpy, os, sys

#geodatabase = arcpy.GetParameterAsText(0)
geodatabase=r"Y:\Sist_Inf_Geo\2017\Subir_Servicios_Geoportal\3EECB_Magna.gdb"
#txtsalida = arcpy.GetParameterAsText(1)
txtsalida=r"C:\temp\salida.txt"
arcpy.env.workspace= geodatabase

datasets=arcpy.ListDatasets()

Fileprj = open (txtsalida, "w")

for dataset in datasets:
    arcpy.env.workspace=geodatabase+os.sep+dataset
    listfc = arcpy.ListFeatureClasses()
    for fc in listfc:
        Fileprj.write(fc.encode("utf-8") + "\n")
Fileprj.close()
