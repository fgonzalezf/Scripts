import arcpy, os, sys
GeodatabaseEntradas=sys.argv[1]
GeodatabaseSalida=sys.argv[2]
GeodatabaseEntradas=GeodatabaseEntradas.split(";")
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf8')
for gdb in GeodatabaseEntradas:
    arcpy.env.workspace=gdb
    arcpy.AddMessage("......Migrando GDB......" + gdb)
    for dataset in arcpy.ListDatasets("*","feature"):
        arcpy.env.workspace=gdb + os.sep+ dataset
        for fc in arcpy.ListFeatureClasses():
            featEnt= gdb + os.sep+ dataset +os.sep+fc
            featSal= GeodatabaseSalida+os.sep+"MapaBase"+os.sep+fc
            result = arcpy.GetCount_management(featEnt)
            count=int(result.getOutput(0))
            arcpy.env.workspace=GeodatabaseSalida+os.sep+"MapaBase"
            #arcpy.AddMessage("Procesando..."+fc)
            if count>0:
                if arcpy.Exists(featSal):
                    try:
                        arcpy.AddMessage("Migrando..."+ fc)
                        arcpy.Append_management(featEnt,featSal,"NO_TEST")
                    except Exception as ex:
                        arcpy.AddMessage("Error Migrando..."+ fc +"..."+ex.message)