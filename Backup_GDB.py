import arcpy, os,sys

arcpy.env.workspace=r"E:\Conexiones_SDE\arcconsulta.sde"

ListaDatasets= arcpy.ListDatasets()
ListaFeaturesClass = arcpy.ListFeatureClasses()
ListaTablas=arcpy.ListTables()
ListaRasters = arcpy.ListRasters()

GeodatabaseSalida =r"E:\BackupD\BK_Arconsulta.gdb"

for dt in ListaDatasets:
    try:

        if arcpy.Exists(GeodatabaseSalida+os.sep+dt.split(".")[1])==False:
            print ("Copiando....." + dt)
            arcpy.Copy_management(dt,GeodatabaseSalida+os.sep+dt)
    except Exception as e:
        print ("Error Copiando....."+ dt + str(e))

for fce in ListaFeaturesClass:
    try:
        if arcpy.Exists(GeodatabaseSalida + os.sep + fce.split(".")[1])==False:
            print ("Copiando....." + fce)

            arcpy.Copy_management(fce,GeodatabaseSalida+os.sep+fce)
    except Exception as e:
        print ("Error Copiando....."+ fce + str(e))

for tab in ListaTablas:
    try:
        if arcpy.Exists(GeodatabaseSalida + os.sep + tab.split(".")[1])==False:
            print ("Copiando....." + tab)
            arcpy.Copy_management(tab,GeodatabaseSalida+os.sep+tab)
    except Exception as e:
        print ("Error Copiando....."+ tab + str(e))

for ras in ListaRasters:
    try:
        if arcpy.Exists(GeodatabaseSalida + os.sep + ras.split(".")[1])==False:
            print ("Copiando....." + ras)
            arcpy.Copy_management(ras,GeodatabaseSalida+os.sep+ras)
    except Exception as e:
        print ("Error Copiando....."+ ras + str(e))