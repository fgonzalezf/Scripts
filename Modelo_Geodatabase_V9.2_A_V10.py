#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-
__author__ = 'fernando.gonzalez'
import arcpy,os,sys
arcpy.env.overwriteOutput=True
Geodatabase=r"D:\Proyecto\fernando.gonzalez\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\25K\CON ANOTACIONES\25K_10_02_2016_GEODATABASE_CARGUE.mdb"
arcpy.env.workspace=Geodatabase

print "Creando Dominios"
arcpy.CreateMosaicDataset_management(Geodatabase,"Modelo_Digital_Terreno","C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Geographic Coordinate Systems\South America\MAGNA.prj","1","32_BIT_FLOAT")


try:
    arcpy.CreateDomain_management(Geodatabase,"Dom_Elevacion","Tipo de Elevacion","TEXT","CODED")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Elevacion","1","Medida")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Elevacion","2","Estimada")
except:
    pass

try:
    arcpy.CreateDomain_management(Geodatabase,"Dom_Fuente_Elevacion","Origen de la información Implementada en el Modelo","TEXT","CODED")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Fuente_Elevacion","1","Lídar")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Fuente_Elevacion","2","Radar")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Fuente_Elevacion","3","Fotogrametría")
except:
    pass
try:
    arcpy.CreateDomain_management(Geodatabase,"Dom_Tipo_Punto_Materializado","Tipo de Punto Materializado","TEXT","CODED")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Punto_Materializado","1","Punto Geodésico")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Punto_Materializado","2","Punto Topográfico")
    arcpy.AddCodedValueToDomain_management(Geodatabase,"Dom_Tipo_Punto_Materializado","3","Punto Nivelación")
except:
    pass
ListaDatasets=arcpy.ListDatasets()

for dataset in ListaDatasets:
    if dataset=="Relieve":
        print "Creando Lineas Demarcación"
        Lineas_Demarcacion_Terreno=arcpy.CreateFeatureclass_management(Geodatabase+os.sep+dataset,"Lineas_Demarcacion_Terreno","POLYLINE","","","ENABLED")
        Puntos_Masa=arcpy.CreateFeatureclass_management(Geodatabase+os.sep+dataset,"Puntos_Masa","POINT","","","ENABLED")
        Modelo_Digital_Terreno_P=arcpy.CreateFeatureclass_management(Geodatabase+os.sep+dataset,"Modelo_Digital_Terreno_P","POINT","","","ENABLED")
        print "Creando  Modelo_Digital_Terreno_P"

        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"TIPO_ELEVACION","TEXT","","","30","TTET","","","Dom_Elevacion")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"FUENTE","TEXT","","","30","FTE","","","Dom_Fuente_Elevacion")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"SYMBOL","TEXT","","","255","Symbol","","","Dom_Gen_PLTS")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"PROYECTO","TEXT","","","30","","","","")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"FECHA","DATE","","","","","","","")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"CAMBIO","TEXT","","","2","","","","Dom_Cambios")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"RESPONSABLE","TEXT","","","100","","","","")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"VIGENCIA","TEXT","","","2","","","","Dom_Vigencia")
        arcpy.AddField_management(Lineas_Demarcacion_Terreno,"FECHA_MODIFICACION","DATE","","","30","","","","")


        arcpy.AddField_management(Modelo_Digital_Terreno_P,"ALTURA_SOBRE_NIVEL_MAR","DOUBLE","","","30","TALT","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"TIPO_ELEVACION","TEXT","","","30","TTET","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"FUENTE","TEXT","","","30","FTE","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"SYMBOL","TEXT","","","255","Symbol","","","Dom_Gen_PLTS")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"PROYECTO","TEXT","","","30","","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"FECHA","DATE","","","","","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"CAMBIO","TEXT","","","2","","","","Dom_Cambios")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"RESPONSABLE","TEXT","","","100","","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"VIGENCIA","TEXT","","","2","","","","Dom_Vigencia")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"FECHA_MODIFICACION","DATE","","","30","","","","")

        print "Creando  Puntos_Masa"

        arcpy.AddField_management(Modelo_Digital_Terreno_P,"COORDENADA_X","DOUBLE","","","","COOR_X","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"COORDENADA_Y","DOUBLE","","","","COOR_Y","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"COORDENADA_Z","DOUBLE","","","","COOR_Z","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"SYMBOL","TEXT","","","255","Symbol","","","Dom_Gen_PLTS")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"PROYECTO","TEXT","","","30","","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"FECHA","DATE","","","","","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"CAMBIO","TEXT","","","2","","","","Dom_Cambios")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"RESPONSABLE","TEXT","","","100","","","","")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"VIGENCIA","TEXT","","","2","","","","Dom_Vigencia")
        arcpy.AddField_management(Modelo_Digital_Terreno_P,"FECHA_MODIFICACION","DATE","","","30","","","","")




    elif dataset=="Puntos_de_Control":

        print "Creando  Puntos_de_Control"
        Punto_Materializado=arcpy.CreateFeatureclass_management(Geodatabase+os.sep+dataset,"Punto_Materializado","POINT","","","ENABLED")
        arcpy.AddField_management(Punto_Materializado,"NOMBRE_PUNTO","DOUBLE","","","","NMP","","","")
        arcpy.AddField_management(Punto_Materializado,"TIPO_PUNTO","TEXT","","","30","","","","Dom_Tipo_Punto_Materializado")
        arcpy.AddField_management(Punto_Materializado,"ALTURA_SOBRE_NIVEL_MAR","DOUBLE","","","","TALT","","","")
        arcpy.AddField_management(Punto_Materializado,"PK_CUE","DOUBLE","","","","","","","")
        arcpy.AddField_management(Punto_Materializado,"SYMBOL","TEXT","","","255","Symbol","","","Dom_Gen_PLTS")
        arcpy.AddField_management(Punto_Materializado,"PROYECTO","TEXT","","","30","","","","")
        arcpy.AddField_management(Punto_Materializado,"FECHA","DATE","","","","","","","")
        arcpy.AddField_management(Punto_Materializado,"CAMBIO","TEXT","","","2","","","","Dom_Cambios")
        arcpy.AddField_management(Punto_Materializado,"RESPONSABLE","TEXT","","","100","","","","")
        arcpy.AddField_management(Punto_Materializado,"VIGENCIA","TEXT","","","2","","","","Dom_Vigencia")
        arcpy.AddField_management(Punto_Materializado,"FECHA_MODIFICACION","DATE","","","30","","","","")

