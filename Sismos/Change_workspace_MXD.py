import arcpy,os,sys

from arcpy import env


env.overwriteOutput = True
mxd=r"C:\Users\fgonzalezf\Documents\SISMOS\servicios_sismos\sismicidad_historica_2\mapa de intensidades.mxd"
old=r"C:\Users\dzornosa\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\sish Produccion.sde"
newworkspace=r"C:\Users\fgonzalezf\Documents\SISMOS\servicios_sismos\SISHTemp.sde"
salida=mxd.replace(".mxd","_temp.mxd")
mxd = arcpy.mapping.MapDocument(mxd)

mxd.findAndReplaceWorkspacePaths(old, newworkspace)
mxd.saveACopy(salida)
del mxd

