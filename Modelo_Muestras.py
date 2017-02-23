#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

import arcpy, os, sys

arcpy.env.overwriteOutput=True
Carpeta=r"C:\Users\Fernando\Documents\Muestras"
arcpy.CreatePersonalGDB_management(Carpeta, "Muestras.mdb")
Geodatabase= Carpeta +os.sep+"Muestras.mdb"

sisref= arcpy.CreateSpatialReference_management(r"C:\Documents and Settings\Fernando\Datos de programa\ESRI\Desktop10.2\ArcMap\Coordinate Systems\Magna.prj")
arcpy.CreateFeatureDataset_management(Geodatabase,"Muestras",sisref)
dataset= Geodatabase+ os.sep+"Muestras"
#Featuare Class
arcpy.AddMessage("creando featuare Class...")
Muestra= arcpy.CreateFeatureclass_management(dataset,"Muestra","POINT")
arcpy.AlterAliasName(Muestra,"Muestra")
Municipios=arcpy.CreateFeatureclass_management(dataset,"Municipios","POLYGON")
Resultado = arcpy.CreateTable_management(Geodatabase,"Resultado")
Muestra_Laboratorio = arcpy.CreateTable_management(Geodatabase,"Muestra_Laboratorio")
Elemento_Propiedad = arcpy.CreateTable_management(Geodatabase,"Elemento_Propiedad")


#CREACION DE CAMPOS

arcpy.AddMessage("creando campos Muestra....")
arcpy.AddField_management(Muestra,"ID_MUESTRA","LONG","","","","Identificador Único de la muestra")
arcpy.AddField_management(Muestra,"COD_MUESTRA_SGC","TEXT","","","30","Código de Muestra SGC")
arcpy.AddField_management(Muestra,"COD_MUESTRA_LABORATORIO","TEXT","","","20","Código de Muestra Laboratorio")
arcpy.AddField_management(Muestra,"FECHA_INGRESO","DATE","","","","Fecha de Ingreso")
arcpy.AddField_management(Muestra,"FECHA_MUESTREO","DATE","","","","Fecha de Muestreo")
arcpy.AddField_management(Muestra,"FK_COD_PLANCHA_IGAC","TEXT","","","10","Código de la Plancha IGAC")
arcpy.AddField_management(Muestra,"FK_TIPO_MUESTRA","SHORT","","","","Tipo de Muestra")
arcpy.AddField_management(Muestra,"OBSERVACIONES","TEXT","","","255","Observaciones")
arcpy.AddField_management(Muestra,"FK_ESTADO_ROCA","SHORT","","","","Estado de la Roca")
arcpy.AddField_management(Muestra,"FK_NOMBRE_ROCA","SHORT","","","","Nombre de Roca")
arcpy.AddField_management(Muestra,"DESCRIPCION_MUESTRA","TEXT","","","255","Descripción de la Muestra")
arcpy.AddField_management(Muestra,"FK_TIPO_ROCA","SHORT","","","","Tipo de Roca")
arcpy.AddField_management(Muestra,"COD_ESTACION","TEXT","","","30","Código de la Estación")
arcpy.AddField_management(Muestra,"FK_NOMBRE_ROCA","SHORT","","","","Nombre de Roca")
arcpy.AddField_management(Muestra,"FK_DEPARTAMENTO","SHORT","","","","Departamento")
arcpy.AddField_management(Muestra,"FK_MUNICIPIO","SHORT","","","","Municipio")
arcpy.AddField_management(Muestra,"FK_AFLUENTE_PRINCIPAL","SHORT","","","","Afluente Principal")
arcpy.AddField_management(Muestra,"COORDENADAS_X_ORIGEN","SHORT","","","","Coordenadas X de Origen")
arcpy.AddField_management(Muestra,"COORDENADAS_Y_ORIGEN","SHORT","","","","Coordenadas Y de Origen")
arcpy.AddField_management(Muestra,"ORIGEN_GEOGRAFICO","SHORT","","","","Origen Geografico")

arcpy.AddMessage("creando campos Municipios....")
arcpy.AddField_management(Municipios,"NOMBRE_DEPARTAMENTO","SHORT","","","","Nombre Departamento")
arcpy.AddField_management(Municipios,"NOMBRE_MUNICIPIO","SHORT","","","","Nombre Municipio")
arcpy.AddField_management(Municipios,"CODIGO_DEPARTAMENTO","SHORT","","","","Código Departamento")
arcpy.AddField_management(Municipios,"CODIGO_MUNICIPIO","SHORT","","","","Código Municipio")

arcpy.AddMessage("creando campos Resultados....")

arcpy.AddField_management(Resultado,"ID_RESULTADO","LONG","","","","Identificador Resultado")
arcpy.AddField_management(Resultado,"VALOR","DOUBLE","","","","Valor")
arcpy.AddField_management(Resultado,"FK_TECNICA_ANALITICA","SHORT","","","","Técnica Analitica")
arcpy.AddField_management(Resultado,"FK_MUESTRA_LABORATORIO","LONG","","","","Muestra de Laboratorio")
arcpy.AddField_management(Resultado,"FK_ELEMENTO_PROPIEDAD","SHORT","","","","Identificador Resultado")
arcpy.AddField_management(Resultado,"VALOR_ARCHIVO","TEXT","","","255","Valor Archivo")
arcpy.AddField_management(Resultado,"FK_TIPO_ANALISIS","TEXT","","","10","Típo analisis")
arcpy.AddField_management(Resultado,"FK_SECADO","SHORT","","","","Tipo de Secado")
arcpy.AddField_management(Resultado,"FK_TRITURADO","SHORT","","","","Tipo de Triturado")
arcpy.AddField_management(Resultado,"FK_TAMIZADO","SHORT","","","","Tipo de Tamizado")
arcpy.AddField_management(Resultado,"FK_PULVERIZADO","SHORT","","","","Tipo de Pulverizado")
arcpy.AddField_management(Resultado,"FK_MALLA_FINAL","SHORT","","","","Malla Final")
arcpy.AddField_management(Resultado,"FECHA_RESULTADO","DATE","","","","Fecha de Resultado")
arcpy.AddField_management(Resultado,"FK_METODO_ENSAYO","SHORT","","","","Metodo de ensayo")
arcpy.AddField_management(Resultado,"FK_ATAQUE_QUIMICO","SHORT","","","","Ataque Químico")
arcpy.AddField_management(Resultado,"FK_PRE_TRATAMIENTO","SHORT","","","","Pre Tratamiento")
arcpy.AddField_management(Resultado,"VALOR_ORIGINAL","TEXT","","","10","Valor Original")
arcpy.AddField_management(Resultado,"OBSERVACIONES","TEXT","","","255","Observaciones")

arcpy.AddMessage("creando campos Muestra Laboratorio....")

arcpy.AddField_management(Muestra_Laboratorio,"ID_MUESTRA_LABORATORIO","LONG","","","","Identificador Muestra de Laboratorio")
arcpy.AddField_management(Muestra_Laboratorio,"DESCRIPCION","TEXT","","","255","Descripcion")
arcpy.AddField_management(Muestra_Laboratorio,"FK_ID_MUESTRA","LONG","","","","Identificador de la Muestra")
arcpy.AddField_management(Muestra_Laboratorio,"FK_PRUEBA_LABORATORIO","SHORT","","","","Pruebas de laboratorio")
arcpy.AddField_management(Muestra_Laboratorio,"FK_LABORATORIO","SHORT","","","","Identificador Laboratorio")
arcpy.AddField_management(Muestra_Laboratorio,"OBSERVACIONES","TEXT","","","255","Observaciones")
arcpy.AddField_management(Muestra_Laboratorio,"COD_MUESTRA_LABORATORIO","TEXT","","","20","Muestra laboratorio")
arcpy.AddField_management(Muestra_Laboratorio,"FECHA_SOLICITUD","DATE","","","","Fecha de Solicitud")
arcpy.AddField_management(Muestra_Laboratorio,"SERVICIOS_SOLICITADOS","TEXT","","","255","Servicios Solicitados")
arcpy.AddField_management(Muestra_Laboratorio,"SERVICIOS_ESPECIALES","TEXT","","","255","Servicios Especiales")
arcpy.AddField_management(Muestra_Laboratorio,"FECHA_RESULTADOS","DATE","","","","Resultados")
arcpy.AddField_management(Muestra_Laboratorio,"FK_SECADO","SHORT","","","","Secado")
arcpy.AddField_management(Muestra_Laboratorio,"FK_TRITURADO","SHORT","","","","Triturado")
arcpy.AddField_management(Muestra_Laboratorio,"FK_TAMIZADO","SHORT","","","","Tamizado")
arcpy.AddField_management(Muestra_Laboratorio,"FK_PULVERIZADO","SHORT","","","","Pulverizado")
arcpy.AddField_management(Muestra_Laboratorio,"FK_MALLA_FINAL","SHORT","","","","Malla Final")
arcpy.AddField_management(Muestra_Laboratorio,"FK_ATAQUE_QUIMICO","SHORT","","","10","Ataque Quimico")
arcpy.AddField_management(Muestra_Laboratorio,"FK_PRE_TRATAMIENTO","SHORT","","","255","Pre Tratamiento")
arcpy.AddField_management(Muestra_Laboratorio,"FK_ID_ESTANTDAR","SHORT","","","","Identificador Estandar")
arcpy.AddField_management(Muestra_Laboratorio,"FK_ALCANCE_ATAQUE","SHORT","","","","Alcance del Ataque")
arcpy.AddField_management(Muestra_Laboratorio,"ID_LAMINA","TEXT","","","20","Identificador Lamina")
arcpy.AddField_management(Muestra_Laboratorio,"FK_TIPO_LAMINA","SHORT","","","","Tipo de Lamina")

arcpy.AddMessage("creando campos Elemento Propiedad....")


arcpy.AddField_management(Elemento_Propiedad,"ID_ELEMENTO_PROPIEDAD","SHORT","","","","Identificador del Elemento propiedad")
arcpy.AddField_management(Elemento_Propiedad,"DESCRIPCION","TEXT","","","50","Descripcion")
arcpy.AddField_management(Elemento_Propiedad,"PK_ID_UNIDAD","SHORT","","","","Identificador de Unidad")

arcpy.CreateRelationshipClass_management(Muestra,Muestra_Laboratorio,Geodatabase+ os.sep+"Muestra_Resultado_Rel","SIMPLE","Atributos de Muestra","Atributos de Muestra Laboratorio","NONE","ONE_TO_MANY","NONE","ID_MUESTRA", "FK_ID_MUESTRA")

