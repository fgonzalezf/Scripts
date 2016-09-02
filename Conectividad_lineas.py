import arcpy, os, sys

LayerConetado=sys.argv[1]
LayerConexion=sys.argv[2]

Puntos_temporales="in_memory/dangles_Iniciales"
Puntos_Finales=os.getenv('APPDATA')+os.sep+LayerConetado+".shp"

LayerSimbologia=r"I:\Documentacion\APLICACIONES_VALIDADAS\ToolBox y Scripts\ToolBox\Conexion_Lineas\Simbologia.lyr"

layer =os.getenv('APPDATA')+os.sep+"Dangles_"+LayerConetado+".lyr"
if arcpy.Exists(Puntos_temporales):
    arcpy.Delete_management(Puntos_temporales)
if arcpy.Exists(Puntos_Finales):
    arcpy.Delete_management(Puntos_Finales)
if arcpy.Exists("Dangles_"+LayerConetado):
    arcpy.Delete_management("Dangles_"+LayerConetado)
if arcpy.Exists(layer):
    arcpy.Delete_management(layer)


arcpy.FeatureVerticesToPoints_management(LayerConetado,Puntos_temporales,"DANGLE")
arcpy.Erase_analysis(Puntos_temporales,LayerConexion,Puntos_Finales,"0.00001 Meters")

arcpy.Delete_management(Puntos_temporales)

mxd = arcpy.mapping.MapDocument("CURRENT")
df=arcpy.mapping.ListDataFrames(mxd)[0]
arcpy.MakeFeatureLayer_management(Puntos_Finales,"Dangles_"+LayerConetado)
if arcpy.Exists(LayerSimbologia):
    arcpy.ApplySymbologyFromLayer_management("Dangles_"+LayerConetado,LayerSimbologia)
arcpy.SaveToLayerFile_management("Dangles_"+LayerConetado,layer)
addLayer = arcpy.mapping.Layer(layer)
arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
del mxd
