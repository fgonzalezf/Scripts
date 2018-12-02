import arcpy, os,sys

Geodatabase=r""
arcpy.env.workspace=Geodatabase

ListaFeatOut=arcpy.ListFeatureClasses()
ListaDatasets=arcpy.ListDatasets()

