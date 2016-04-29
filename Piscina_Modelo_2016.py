#!/usr/bin/python
# -*- coding: latin-1 -*-
import arcpy, os,sys


Geodatabase=r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\V10.1\TEMP\Proyectadas\25K_Con_Anotaciones\25K_10_02_2016_GEODATABASE_CARGUE.mdb"
LayerRep=r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\V10.1\10K_Gobernacion\con_anotaciones\Piscina.lyr"
arcpy.env.workspace=Geodatabase

#Borrado Capa
print "Borrando..."
arcpy.Delete_management(Geodatabase+os.sep+"Edificacion_ObraCivil"+os.sep+"Piscina")
#Creando nuevo capa
try:
    arcpy.CreateDomain_management(Geodatabase,"Dom_Tipo_Piscina","Clasificación de Piscinas","TEXT","CODED")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Piscina","3901","Agrícola")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Piscina","3902","Industrial")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Piscina","3903","Recreacional")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Piscina","3904","Otros Usos")
    #Agrícola, Industrial, Recreacional y Otros Usos.
except:
    print "Dominio Ya Creado..."
    pass

print "Creando..."
PiscinaFT=arcpy.CreateFeatureclass_management(Geodatabase+os.sep+"Edificacion_ObraCivil","Piscina","POLYGON","","","ENABLED")

arcpy.AddField_management(PiscinaFT,"TIPO","TEXT","","","30","","","","Dom_Tipo_Piscina")
arcpy.AddField_management(PiscinaFT,"SYMBOL","TEXT","","","255","Symbol","","","Dom_Gen_PLTS")
arcpy.AddField_management(PiscinaFT,"PROYECTO","TEXT","","","30","","","","")
arcpy.AddField_management(PiscinaFT,"FECHA","DATE","","","","","","","")
arcpy.AddField_management(PiscinaFT,"PKCUE","DOUBLE","","","","","","","")
arcpy.AddField_management(PiscinaFT,"CAMBIO","TEXT","","","2","","","","Dom_Cambios")
arcpy.AddField_management(PiscinaFT,"RESPONSABLE","TEXT","","","100","","","","")
arcpy.AddField_management(PiscinaFT,"VIGENCIA","TEXT","","","2","","","","Dom_Vigencia")
arcpy.AddField_management(PiscinaFT,"FECHA_MODIFICACION","DATE","","","30","","","","")

arcpy.AddRepresentation_cartography(Geodatabase+os.sep+"Edificacion_ObraCivil"+os.sep+"Piscina","Piscina"+"_Rep","RuleID","Override","STORE_CHANGE_AS_OVERRIDE",LayerRep,"ASSIGN")