import arcpy, os, uuid
#points = arcpy.GetParameterAsText(0)
layer = arcpy.GetParameterAsText(0)
kmzName="KMZ_EXPORT"+str(uuid.uuid4()).replace("-","")[:10]+".kmz"
salida =r"\\FGF\Plantillas"+os.sep+kmzName
salidalayer =r"\\FGF\Plantillas"+os.sep+"Layer"+str(uuid.uuid4()).replace("-","")[:10]+".lyr"
arcpy.MakeFeatureLayer_management(layer,"LayerConvert")
arcpy.SaveToLayerFile_management("LayerConvert",salidalayer)
urlsalida="http://fgf/kml/"+kmzName
arcpy.LayerToKML_conversion(salidalayer,salida,0)
arcpy.AddMessage(urlsalida)
arcpy.SetParameterAsText(1,urlsalida)

