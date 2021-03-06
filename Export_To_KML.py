import arcpy, os, uuid, locale
locale.setlocale(locale.LC_ALL,"english")
#points = arcpy.GetParameterAsText(0)
layer = arcpy.GetParameterAsText(0)
kmzName="KMZ_EXPORT"+str(uuid.uuid4()).replace("-","")[:10]+".kmz"
salida =r"\\Srvarcgis10\kmlsismos"+os.sep+kmzName
salidalayer =r"\\Srvarcgis10\kmlsismos"+os.sep+"Layer"+str(uuid.uuid4()).replace("-","")[:10]+".lyr"
arcpy.MakeFeatureLayer_management(layer,"LayerConvert")
arcpy.SaveToLayerFile_management("LayerConvert",salidalayer)
urlsalida="http://srvags.sgc.gov.co/Archivos_Geoportal/KMLSISMOS/"+kmzName
arcpy.LayerToKML_conversion(salidalayer,salida,0)
arcpy.AddMessage(urlsalida)
arcpy.SetParameterAsText(1,urlsalida)

