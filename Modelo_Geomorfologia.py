#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

import arcpy, os, sys

arcpy.env.overwriteOutput=True
Carpeta=r"C:\Users\fgonzalezf\Documents\Geomorfologia\BaseDatos"
arcpy.CreatePersonalGDB_management(Carpeta, "Geomorfologia.mdb")
Geodatabase= Carpeta +os.sep+"Geomorfologia.mdb"

sisref= arcpy.CreateSpatialReference_management(r"C:\Documents and Settings\Fernando\Datos de programa\ESRI\Desktop10.2\ArcMap\Coordinate Systems\Magna.prj")
arcpy.CreateFeatureDataset_management(Geodatabase,"Geomorfologia",sisref)
dataset= Geodatabase+ os.sep+"Geomorfologia"
#Featuare Class
arcpy.AddMessage("creando featuare Class...")
UMG= arcpy.CreateFeatureclass_management(dataset,"UMG","POLYGON")
ContactoGeomorfologico=arcpy.CreateFeatureclass_management(dataset,"ContactoGeomorfologico","POLYLINE")
RasgosGeomorfologicos_L=arcpy.CreateFeatureclass_management(dataset,"RasgosGeomorfologicos_L","POLYLINE")
ProcesosGeomorfologico=arcpy.CreateFeatureclass_management(dataset,"ProcesosGeomorfologico_L","POLYLINE")
ProcesosGeomorfologico_P=arcpy.CreateFeatureclass_management(dataset,"ProcesosGeomorfologico_P","POINT")
RasgosGeomorfologicos_P=arcpy.CreateFeatureclass_management(dataset,"RasgosGeomorfologicos_P","POINT")
BocasVolcan=arcpy.CreateFeatureclass_management(dataset,"BocasVolcan","POINT")

#CREACION DE CAMPOS

arcpy.AddMessage("creando campos UMG....")
arcpy.AddField_management(UMG,"SimboloUGM","TEXT","","","20","Símbolo UGM")
arcpy.AddField_management(UMG,"No_CartaColores","TEXT","","","10","No CartaColores")
arcpy.AddField_management(UMG,"GeoformoEstructura","TEXT","","","255","Geoformo Estructura")
arcpy.AddField_management(UMG,"Provincia","TEXT","","","255","Provincia")
arcpy.AddField_management(UMG,"Subunidades","TEXT","","","255","Subunidades")
arcpy.AddField_management(UMG,"Componente","TEXT","","","255","Componente")
arcpy.AddField_management(UMG,"AmbienteMorfogenetico","TEXT","","","50","Ambiente Morfogenetico")
arcpy.AddField_management(UMG,"TipoMaterial","TEXT","","","255","Tipo Material")
arcpy.AddField_management(UMG,"Morfologia","TEXT","","","255","Morfologia")
arcpy.AddField_management(UMG,"Edad","TEXT","","","50","Edad")
arcpy.AddField_management(UMG,"Descripcion","TEXT","","","255","Descripción")
arcpy.AddField_management(UMG,"Comentarios","TEXT","","","255","Comentarios")

arcpy.AddMessage("creando campos ContactoGeomorfologico....")
arcpy.AddField_management(ContactoGeomorfologico,"Contacto","TEXT","","","50")
arcpy.AddField_management(ContactoGeomorfologico,"ExactitudLocalizacion","TEXT","","","50","Exactitud Localización")
arcpy.AddField_management(ContactoGeomorfologico,"Comentarios","TEXT","","","255","Comentarios")
arcpy.AddMessage("creando campos RasgosGeomorfologicos....")
arcpy.AddField_management(RasgosGeomorfologicos_L,"Tipo","TEXT","","","50","Tipo")
arcpy.AddField_management(RasgosGeomorfologicos_L,"ExactitudLocalizacion","TEXT","","","50","Exactitud Localización")
arcpy.AddField_management(RasgosGeomorfologicos_L,"Comentarios","TEXT","","","255","Comentarios")
arcpy.AddMessage("creando campos ProcesosGeomorfologico....")
arcpy.AddField_management(ProcesosGeomorfologico,"Tipo","TEXT","","","50","Tipo")
arcpy.AddField_management(ProcesosGeomorfologico,"ExactitudLocalizacion","TEXT","","","50","Exactitud Localización")
arcpy.AddField_management(ProcesosGeomorfologico,"Comentarios","TEXT","","","255","Comentarios")
arcpy.AddMessage("creando campos ProcesosGeomorfologico_P....")
arcpy.AddField_management(ProcesosGeomorfologico_P,"Tipo","TEXT","","","50","Tipo")
arcpy.AddField_management(ProcesosGeomorfologico_P,"NombreEstacion","TEXT","","","50","Nombre de la estación")
arcpy.AddField_management(ProcesosGeomorfologico_P,"Descripcion","TEXT","","","255","Descripción")
arcpy.AddField_management(ProcesosGeomorfologico_P,"Comentarios","TEXT","","","255","Comentarios")
arcpy.AddField_management(ProcesosGeomorfologico_P,"Rotacion","DOUBLE","","","","Rotación")
arcpy.AddField_management(RasgosGeomorfologicos_P,"Visibilidad","TEXT","","","10","Visibilidad")


arcpy.AddMessage("creando campos RasgosGeomorfologicos_P....")
arcpy.AddField_management(RasgosGeomorfologicos_P,"Tipo","TEXT","","","20","Tipo")
arcpy.AddField_management(RasgosGeomorfologicos_P,"NombreEstacion","TEXT","","","12","Nombre Estación")
#arcpy.AddField_management(RasgosGeomorfologicos_P,"UGMMedida","TEXT","","","60","UGM Medida")
arcpy.AddField_management(RasgosGeomorfologicos_P,"Comentarios","TEXT","","","255","Comentarios")
arcpy.AddField_management(RasgosGeomorfologicos_P,"Visibilidad","TEXT","","","10","Visibilidad")
arcpy.AddMessage("creando campos BocasVolcan....")
arcpy.AddField_management(BocasVolcan,"Tipo","TEXT","","","20","Tipo")
arcpy.AddField_management(BocasVolcan,"NombreEstacion","TEXT","","","12","Nombre Estación")
#arcpy.AddField_management(BocasVolcan,"UGMMedida","TEXT","","","60","UGM Medida")
arcpy.AddField_management(BocasVolcan,"Descripcion","TEXT","","","255","Descripción")
arcpy.AddField_management(BocasVolcan,"Comentarios","TEXT","","","255","Comentarios")
arcpy.AddField_management(BocasVolcan,"Visibilidad","TEXT","","","10","Visibilidad")


#Creacion de Dominios
arcpy.env.workspace=r"C:\Users\fgonzalezf\Documents\Geomorfologia\BaseDatos\Dominios.mdb"
listaTablas = arcpy.ListTables()

for tabla in listaTablas:
    arcpy.AddMessage("creando dominio: "+ tabla)
    arcpy.TableToDomain_management(tabla,"codigo","descripcion",Geodatabase,tabla)
    if tabla == "Dom_Ambiente_Morfogenetico":
        arcpy.AssignDomainToField_management(UMG,"AmbienteMorfogenetico",tabla)
    elif tabla == "Dom_Contacto_Exactitud_Posicion":
        arcpy.AssignDomainToField_management(ContactoGeomorfologico,"ExactitudLocalizacion",tabla)
    elif tabla == "Dom_Exactitud_Localizacion":
        arcpy.AssignDomainToField_management(RasgosGeomorfologicos_L,"ExactitudLocalizacion",tabla)
        arcpy.AssignDomainToField_management(ProcesosGeomorfologico,"ExactitudLocalizacion",tabla)
    elif tabla == "Dom_Tipo_Bocas_Volcan":
        arcpy.AssignDomainToField_management(BocasVolcan,"Tipo",tabla)
    elif tabla == "Dom_Tipo_Material":
        arcpy.AssignDomainToField_management(UMG,"TipoMaterial",tabla)
    elif tabla == "Dom_Tipo_Proceso_Geomorfologico_Linea":
        arcpy.AssignDomainToField_management(ProcesosGeomorfologico,"Tipo",tabla)
    elif tabla == "Dom_Tipo_Proceso_Geomorfologico_Punto":
        arcpy.AssignDomainToField_management(ProcesosGeomorfologico_P,"Tipo",tabla)
    elif tabla == "Dom_Tipo_Rasgo_Geomorfologico_Lnea":
        arcpy.AssignDomainToField_management(RasgosGeomorfologicos_L,"Tipo",tabla)
    elif tabla == "Dom_Tipo_Rasgo_Geomorfologico_Punto":
        arcpy.AssignDomainToField_management(RasgosGeomorfologicos_P,"Tipo",tabla)
    elif tabla == "Dom_Visibilidad":
        arcpy.AssignDomainToField_management(RasgosGeomorfologicos_P,"Visibilidad",tabla)
        arcpy.AssignDomainToField_management(BocasVolcan,"Visibilidad",tabla)
        arcpy.AssignDomainToField_management(RasgosGeomorfologicos_P,"Visibilidad",tabla)

arcpy.AddMessage("Exportando GDB")
arcpy.CreatePersonalGDB_management(Carpeta,"Geomorfologia_Export.mdb")
arcpy.ExportXMLWorkspaceDocument_management(Geodatabase,Carpeta+os.sep+"Wxml.xml")
arcpy.ImportXMLWorkspaceDocument_management(Carpeta+os.sep+"Geomorfologia_Export.mdb",Carpeta+os.sep+"Wxml.xml","SCHEMA_ONLY")
arcpy.Delete_management(Carpeta+os.sep+"Wxml.xml")