#!/usr/bin/python
# -*- coding: latin-1 -*-
import arcpy,os

Geodatabase=r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.3_18_04_2016\25K\Anotaciones\25K_08_04_2016_GEODATABASE_ANOTACIONES.mdb"

arcpy.env.workspace= Geodatabase
Listadatasets = arcpy.ListDatasets()

for dataset in Listadatasets:
    arcpy.env.workspace=Geodatabase+ os.sep+ dataset
    ListaFeat= arcpy.ListFeatureClasses()
    for fc in ListaFeat:
        Desc= arcpy.Describe(fc)
        arcpy.AlterField_management(fc, "PLANCHA", "HOJA", "HOJA")
        #if Desc.featureType != "Annotation":
        print fc
