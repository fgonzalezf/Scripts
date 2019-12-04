import arcpy, os,sys

GeodatabaseEntrada = r"E:\Scripts\GDB\geoprocesos\Geoprocesos.gdb"


Ceventos = GeodatabaseEntrada+ os.sep+"DAICMA"+os.sep+ "Eventos"
Cmunicipios = GeodatabaseEntrada+ os.sep+"DAICMA"+os.sep+ "Municipios"
Cconsejos = GeodatabaseEntrada+ os.sep+"RESGUARDOS_INDIGENAS"+os.sep+ "Consejos_Comunitarios_Negros_2019"
Cresguardos = GeodatabaseEntrada+ os.sep+"RESGUARDOS_INDIGENAS"+os.sep+ "Resguardos_IndIgenas_2019"

Cconsejosint = GeodatabaseEntrada+ os.sep+"Geoprocesos"+os.sep+ "Consejos_Afectacion"
Cresguardosint = GeodatabaseEntrada+ os.sep+"Geoprocesos"+os.sep+ "Resguardos_Afectacion"

print "Iniciando Proceso"
arcpy.DeleteFeatures_management(Cconsejosint)
arcpy.DeleteFeatures_management(Cresguardosint)
#arcpy.SpatialJoin_analysis(FeatIn , FeatJoin ,FeatOut,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
FeatOutC = """in_memory\\consejos"""
FeatOutR = """in_memory\\resguardos"""
arcpy.Intersect_analysis([Cmunicipios,Cconsejos],FeatOutC,"",1.5)
arcpy.Intersect_analysis([Cmunicipios,Cresguardos],FeatOutR)




arcpy.Append_management(FeatOutC,Cconsejosint,"NO_TEST")
arcpy.Append_management(FeatOutR,Cresguardosint,"NO_TEST")

fields=["Afectacion_No_Eventos","SHAPE@"]
X=0
with arcpy.da.UpdateCursor(Cconsejosint, fields) as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management(Ceventos,"EventsTemp","""estatus = 'Abierto'""")
        arcpy.SelectLayerByLocation_management("EventsTemp","INTERSECT",row[1],"","NEW_SELECTION")
        result = arcpy.GetCount_management("EventsTemp")
        count = int(result.getOutput(0))
        row[0]=count
        arcpy.Delete_management("EventsTemp")
        X=X+1
        print(X)
        cursor.updateRow(row)
X=0
with arcpy.da.UpdateCursor(Cresguardosint, fields) as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management(Ceventos,"EventsTemp","""estatus = 'Abierto'""")
        arcpy.SelectLayerByLocation_management("EventsTemp","INTERSECT",row[1],"","NEW_SELECTION")
        result = arcpy.GetCount_management("EventsTemp")
        count = int(result.getOutput(0))
        row[0]=count
        arcpy.Delete_management("EventsTemp")
        X=X+1
        print(X)
        cursor.updateRow(row)


del FeatOutC
del FeatOutR