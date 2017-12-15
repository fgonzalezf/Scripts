import arcpy, os, uuid,locale


#points = arcpy.GetParameterAsText(0)

layer = arcpy.GetParameterAsText(0)

kmzName="KMZEXPORT"+str(uuid.uuid4()).replace("-","")[:10]+".xls"

salida ="\\\\Srvarcgis10\\kmlsismos"+os.sep+kmzName

salidalayer ="\\\\Srvarcgis10\\kmlsismos"+os.sep+"Layer"+str(uuid.uuid4()).replace("-","")[:10]+".lyr"

arcpy.AddMessage(salidalayer)

arcpy.MakeFeatureLayer_management(layer,"LayerConvert")

arcpy.SaveToLayerFile_management("LayerConvert",salidalayer)

urlsalida="http://srvags.sgc.gov.co/Archivos_Geoportal/KMLSISMOS/"+kmzName

locale.setlocale(locale.LC_ALL,"american")

arcpy.TableToExcel_conversion(salidalayer,salida)

arcpy.AddMessage(urlsalida)

arcpy.SetParameterAsText(1,urlsalida)
