# -*- coding: utf-8 -*-
import arcpy, os,sys

GeodatabaseEntrada = r"E:\Scripts\GDB\geoprocesos\Geoprocesos.gdb"


Ceventos = r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Eventos"
Cmunicipios = r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Municipios"
Cconsejos = r"E:\Scripts\SDE.sde\SDE.DBO.RESGUARDOS_INDIGENAS\SDE.DBO.Consejos_Comunitarios_Negros_2019"
Cresguardos = r"E:\Scripts\SDE.sde\SDE.DBO.RESGUARDOS_INDIGENAS\SDE.DBO.Resguardos_IndIgenas_2019"

Cconsejosint = GeodatabaseEntrada+ os.sep+"Geoprocesos"+os.sep+ "Consejos_Afectacion"
Cresguardosint = GeodatabaseEntrada+ os.sep+"Geoprocesos"+os.sep+ "Resguardos_Afectacion"

print "Iniciando Proceso"
arcpy.DeleteFeatures_management(Cconsejosint)
arcpy.DeleteFeatures_management(Cresguardosint)
#arcpy.SpatialJoin_analysis(FeatIn , FeatJoin ,FeatOut,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
FeatOutC = """in_memory\\consejos"""
FeatOutR = """in_memory\\resguardos"""
arcpy.Intersect_analysis([Cmunicipios,Cconsejos],FeatOutC,"",0.0000001)
arcpy.Intersect_analysis([Cmunicipios,Cresguardos],FeatOutR,"",0.0000001)




arcpy.Append_management(FeatOutC,Cconsejosint,"NO_TEST")
arcpy.Append_management(FeatOutR,Cresguardosint,"NO_TEST")

fields=["Afectacion_No_Eventos","SHAPE@","Afectacion_No_Eventos_CR","Afectacion_No_Eventos_IN"]
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
X=0
with arcpy.da.UpdateCursor(Cconsejosint, fields) as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management(Ceventos,"EventsTemp","""estatus = 'Cerrado'""")
        arcpy.SelectLayerByLocation_management("EventsTemp","INTERSECT",row[1],"","NEW_SELECTION")
        result = arcpy.GetCount_management("EventsTemp")
        count = int(result.getOutput(0))
        row[2]=count
        arcpy.Delete_management("EventsTemp")
        X=X+1
        print(X)
        cursor.updateRow(row)
X=0
with arcpy.da.UpdateCursor(Cresguardosint, fields) as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management(Ceventos,"EventsTemp","""estatus = 'Cerrado'""")
        arcpy.SelectLayerByLocation_management("EventsTemp","INTERSECT",row[1],"","NEW_SELECTION")
        result = arcpy.GetCount_management("EventsTemp")
        count = int(result.getOutput(0))
        row[2]=count
        arcpy.Delete_management("EventsTemp")
        X=X+1
        print(X)
        cursor.updateRow(row)
X=0
with arcpy.da.UpdateCursor(Cconsejosint, fields) as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management(Ceventos,"EventsTemp","""estatus = 'Recolección de información'""")
        arcpy.SelectLayerByLocation_management("EventsTemp","INTERSECT",row[1],"","NEW_SELECTION")
        result = arcpy.GetCount_management("EventsTemp")
        count = int(result.getOutput(0))
        row[3]=count
        arcpy.Delete_management("EventsTemp")
        X=X+1
        print(X)
        cursor.updateRow(row)
X=0
with arcpy.da.UpdateCursor(Cresguardosint, fields) as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management(Ceventos,"EventsTemp","""estatus =  'Recolección de información'""")
        arcpy.SelectLayerByLocation_management("EventsTemp","INTERSECT",row[1],"","NEW_SELECTION")
        result = arcpy.GetCount_management("EventsTemp")
        count = int(result.getOutput(0))
        row[3]=count
        arcpy.Delete_management("EventsTemp")
        X=X+1
        print(X)
        cursor.updateRow(row)
del FeatOutC
del FeatOutR