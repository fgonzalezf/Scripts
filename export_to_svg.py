#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcpy, os


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


ShapeFile=r"E:\Users\fgonzalezf\Documents\Visor_Volcanes_Portal\Volcanes_URL.shp"
carpeta=r"C:\Temp"
mxd = arcpy.mapping.MapDocument(r"C:\temp\Volacanes.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

valores =unique_values(ShapeFile,"NOMBREVOLC")
for lyr in arcpy.mapping.ListLayers(mxd,"Volcanes_URL", df):
    for val in valores:
        print val
        lyr.definitionQuery=""""NOMBREVOLC" ="""+ "'"+val+"'"
        mxd.save()
        arcpy.mapping.ExportToSVG(mxd,  carpeta+os.sep+val, df,df_export_width=2649,df_export_height=1896)
        #arcpy.mapping.ExportToPNG(mxd,  carpeta+os.sep+val, df,df_export_width=2649,df_export_height=1896,resolution=96)


del mxd