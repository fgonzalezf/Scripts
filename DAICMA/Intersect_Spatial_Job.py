# -*- coding: utf-8 -*-
import arcpy, os,sys

GeodatabaseEntrada = r"E:\Scripts\EFESIOS.sde"


Ceventos = r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Eventos"
Cmunicipios = r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Municipios"
Cconsejos = r"E:\Scripts\EFESIOS.sde\SDE.DBO.RESGUARDOS_INDIGENAS\SDE.DBO.Consejos_Comunitarios_Negros"
Cresguardos = r"E:\Scripts\EFESIOS.sde\SDE.DBO.RESGUARDOS_INDIGENAS\SDE.DBO.Resguardos_Indigenas"
Czonas=r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Zonas"

Cconsejosint = GeodatabaseEntrada+ os.sep+"Geoprocesos"+os.sep+ "Consejos_Afectacion"
Cresguardosint = GeodatabaseEntrada+ os.sep+"Geoprocesos"+os.sep+ "Resguardos_Afectacion"


def ValoresEntrada(Feat,fields):
    datos = {}
    tindx=0
    indx = 0
    CampoIdentificador="OBJECTID_1"
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[indx]] =row
    return datos
#Creacion de Campo

def CalculoCampo (Feat,Campo,Tabla):
    objId="OBJECTID"
    objIdUn="OBJECTID_1"
    fields=[]
    fields.append(objId)
    fields.append(Campo)
    indx = fields.index(objId)
    valoresEntrada = ValoresEntrada(Tabla, ["OBJECTID_1","PNT_COUNT"])
    result = arcpy.GetCount_management(Tabla)
    count = int(result.getOutput(0))
    Numerador = 0
    edit = arcpy.da.Editor(GeodatabaseEntrada)
    edit.startEditing()
    edit.startOperation()
    Controlvalores = []
    with arcpy.da.UpdateCursor(Feat, fields) as cursor:
        for row in cursor:
            keyvalue = row[indx]
            if keyvalue in valoresEntrada:
                if keyvalue not in Controlvalores:
                    try:
                        Numerador = Numerador + 1
                        print "Actualizando Valor..." + str(row[indx]) + "....(" + str(Numerador) + " de " + str(
                            count) + ")"
                        cursor.updateRow(valoresEntrada[keyvalue])
                        Controlvalores.append(keyvalue)
                    except Exception as e:
                        print "Error..." + e.message
    edit.stopOperation()
    edit.stopEditing("True")




print "Iniciando Proceso"
arcpy.DeleteFeatures_management(Cconsejosint)
arcpy.DeleteFeatures_management(Cresguardosint)
#arcpy.SpatialJoin_analysis(FeatIn , FeatJoin ,FeatOut,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
FeatTempCM = """in_memory\\consejosCM"""
FeatTempRM = """in_memory\\resguardosRM"""
FeatTempCZ = """in_memory\\consejosCZ"""
FeatTempRZ = """in_memory\\resguardosRZ"""
FeatTempCMZ = """in_memory\\consejosCMZ"""
FeatTempRMZ = """in_memory\\resguardosCMZ"""

print "Primera interseccion..."
arcpy.Intersect_analysis([Cmunicipios,Cconsejos],FeatTempCM,"",0.0000001)
arcpy.Intersect_analysis([Cmunicipios,Cresguardos],FeatTempRM,"",0.0000001)
print "Segunda interseccion..."
arcpy.Intersect_analysis([Czonas,Cconsejos],FeatTempCZ,"",0.0000001)
arcpy.Intersect_analysis([Czonas,Cresguardos],FeatTempRZ,"",0.0000001)
print "Union entre Intersecciones..."
arcpy.Union_analysis([FeatTempCM,FeatTempCZ],FeatTempCMZ,"",0.0000001)
arcpy.Union_analysis([FeatTempRM,FeatTempRZ],FeatTempRMZ,"",0.0000001)



print "Cargue a Geodatabase..."
arcpy.Append_management(FeatTempCMZ,Cconsejosint,"NO_TEST")
arcpy.Append_management(FeatTempRMZ,Cresguardosint,"NO_TEST")


TablaTempConsejosAbiertos = """in_memory\\estadisticasConsejosAbiertos"""
TablaTempResguardosAbiertos = """in_memory\\estadisticasResguardosAbiertos"""
TablaTempConsejosCerrados = """in_memory\\estadisticasConsejosCerrados"""
TablaTempResguardosCerrados = """in_memory\\estadisticasResguardosCerrados"""
TablaTempConsejosRecoleccion = """in_memory\\estadisticasConsejosRecoleccion"""
TablaTempResguardosRecoleccion = """in_memory\\estadisticasResguardosRecoleccion"""

TablaTempConsejosTotal = """in_memory\\estadisticasConsejosTotal"""
TablaTempResguardosTotal = """in_memory\\estadisticasResguardosTotal"""
print "Filtrando Eventos..."
eventosCerrados = arcpy.MakeFeatureLayer_management(Ceventos,"eventosCerrados","""estatus = 'Cerrado'""")
eventosAbiertos = arcpy.MakeFeatureLayer_management(Ceventos,"eventosAbiertos","""estatus = 'Abierto'""")
eventosRecoleccion = arcpy.MakeFeatureLayer_management(Ceventos,"eventosRecoleccion","""estatus = 'Recolección de información'""")
print "Intersecciones espaciales..."
arcpy.TabulateIntersection_analysis(Cconsejosint,"OBJECTID",eventosCerrados,TablaTempConsejosCerrados)
arcpy.TabulateIntersection_analysis(Cconsejosint,"OBJECTID",eventosAbiertos,TablaTempConsejosAbiertos)
arcpy.TabulateIntersection_analysis(Cconsejosint,"OBJECTID",eventosRecoleccion,TablaTempConsejosRecoleccion)
arcpy.TabulateIntersection_analysis(Cconsejosint,"OBJECTID",Ceventos,TablaTempConsejosTotal)

arcpy.TabulateIntersection_analysis(Cresguardosint,"OBJECTID",eventosCerrados,TablaTempResguardosCerrados)
arcpy.TabulateIntersection_analysis(Cresguardosint,"OBJECTID",eventosAbiertos,TablaTempResguardosAbiertos)
arcpy.TabulateIntersection_analysis(Cresguardosint,"OBJECTID",eventosRecoleccion,TablaTempResguardosRecoleccion)
arcpy.TabulateIntersection_analysis(Cresguardosint,"OBJECTID",Ceventos,TablaTempResguardosTotal)
print "Calculando Campos..."
CalculoCampo(Cresguardosint,"Afectacion_No_Eventos_CR",TablaTempResguardosCerrados)
CalculoCampo(Cresguardosint,"Afectacion_No_Eventos_AB",TablaTempResguardosAbiertos)
CalculoCampo(Cresguardosint,"Afectacion_No_Eventos_IN",TablaTempResguardosRecoleccion)
CalculoCampo(Cresguardosint,"Afectacion_No_Eventos_Totales",TablaTempResguardosTotal)


CalculoCampo(Cconsejosint,"Afectacion_No_Eventos_CR",TablaTempConsejosCerrados)
CalculoCampo(Cconsejosint,"Afectacion_No_Eventos_AB",TablaTempConsejosAbiertos)
CalculoCampo(Cconsejosint,"Afectacion_No_Eventos_IN",TablaTempConsejosRecoleccion)
CalculoCampo(Cconsejosint,"Afectacion_No_Eventos_Totales",TablaTempConsejosTotal)


del FeatTempCM
del FeatTempRM
del FeatTempCZ
del FeatTempRZ
del FeatTempCMZ
del FeatTempRMZ

del TablaTempConsejosAbiertos
del TablaTempResguardosAbiertos
del TablaTempConsejosCerrados
del TablaTempResguardosCerrados
del TablaTempConsejosRecoleccion
del TablaTempResguardosRecoleccion
del TablaTempConsejosTotal
del TablaTempResguardosTotal