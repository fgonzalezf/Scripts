import arcpy, os, uuid,locale


#points = arcpy.GetParameterAsText(0)

layer = arcpy.GetParameterAsText(0)

kmzName=layer.split("\\")[-1]+str(uuid.uuid4()).replace("-","")[:10]+".xls"

salida ="\\\\EFESIOS\\ExcelExport"+os.sep+kmzName

#salidalayer ="\\\\EFESIOS\\ExcelExport"+os.sep+"Layer"+str(uuid.uuid4()).replace("-","")[:10]+".lyr"

arcpy.AddMessage(kmzName)

arcpy.AddMessage(layer)

urlsalida="http://ergit.presidencia.gov.co/ExportExcel/"+kmzName

locale.setlocale(locale.LC_ALL,"american")

arcpy.TableToExcel_conversion(layer,salida)

arcpy.AddMessage(urlsalida)

descarga = """<a href="""+urlsalida+""">Excel de Salida</a>"""

arcpy.AddMessage(descarga)

arcpy.SetParameterAsText(1,descarga)
