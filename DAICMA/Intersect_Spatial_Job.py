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
TablaTempConsejosAbiertos = """in_memory\\estadisticasConsejosAbiertos"""
TablaTempResguardosAbiertos = """in_memory\\estadisticasResguardosAbiertos"""
TablaTempConsejosCerrados = """in_memory\\estadisticasConsejosCerrados"""
TablaTempResguardosCerrados = """in_memory\\estadisticasResguardosCerrados"""
TablaTempConsejosRecoleccion = """in_memory\\estadisticasConsejosRecoleccion"""
TablaTempResguardosRecoleccion = """in_memory\\estadisticasResguardosRecoleccion"""

arcpy.TabulateIntersection_analysis(FeatOutC,"ObjectID",Ceventos,TablaTempConsejos,)

del FeatOutC
del FeatOutR