#!/usr/bin/python
# -*- coding: ISO-8859-1 -*-

import arcpy, os, sys

arcpy.env.overwriteOutput=True
Carpeta=r"C:\Users\fgonzalezf\Documents\Muestras\Muestras"
arcpy.CreatePersonalGDB_management(Carpeta, "Muestras.mdb")
Geodatabase= Carpeta +os.sep+"Muestras.mdb"
ModeloReducido=True

sisref= arcpy.CreateSpatialReference_management(r"C:\Documents and Settings\Fernando\Datos de programa\ESRI\Desktop10.2\ArcMap\Coordinate Systems\Magna.prj")
arcpy.CreateFeatureDataset_management(Geodatabase,"Muestras",sisref)
dataset= Geodatabase+ os.sep+"Muestras"
#Featuare Class
arcpy.AddMessage("creando featuare Class...")
Muestra= arcpy.CreateFeatureclass_management(dataset,"Muestra","POINT")
arcpy.AlterAliasName(Muestra,"Muestra")
Resultado = arcpy.CreateTable_management(Geodatabase,"Resultado")
Muestra_Laboratorio = arcpy.CreateTable_management(Geodatabase,"Muestra_Laboratorio")
Elemento_Propiedad = arcpy.CreateTable_management(Geodatabase,"Elemento_Propiedad")

#tablas opcionales
if ModeloReducido !=True:
    Detalle_Muestra = arcpy.CreateTable_management(Geodatabase,"Detalle_Muestra")
    Tipo_Muestra = arcpy.CreateTable_management(Geodatabase,"Tipo_Muestra")
    Caracteristica = arcpy.CreateTable_management(Geodatabase,"Caracteristica")
    Caracteristica_Dominio = arcpy.CreateTable_management(Geodatabase,"Caracteristica_Dominio")
    Pozo = arcpy.CreateTable_management(Geodatabase,"Pozo")
    Litologia_Pozo = arcpy.CreateTable_management(Geodatabase,"Litologia_Pozo")
    Estructura = arcpy.CreateTable_management(Geodatabase,"Estructura")
    Survey = arcpy.CreateTable_management(Geodatabase,"Survey")
    Assay = arcpy.CreateTable_management(Geodatabase,"Assay")
    Detalle_Registro_Pozo = arcpy.CreateTable_management(Geodatabase,"Detalle_Registro_Pozo")
    Recovery = arcpy.CreateTable_management(Geodatabase,"Recovery")
#CREACION DE CAMPOS

arcpy.AddMessage("creando campos Muestra....")
arcpy.AddField_management(Muestra,"ID_MUESTRA","LONG","","","","Identificador Único de la muestra")
arcpy.AddField_management(Muestra,"IGM","TEXT","","","30","Código IGM")
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


if ModeloReducido != True:
    arcpy.AddMessage("creando campos Detalle Muestra....")

    arcpy.AddField_management(Elemento_Propiedad,"ID_DETALLE_MUESTRA","LONG","","","","Identificador del Elemento propiedad")
    arcpy.AddField_management(Elemento_Propiedad,"FK_ID_MUESTRA","LONG","","","","Descripcion")
    arcpy.AddField_management(Elemento_Propiedad,"FK_CARACTERISTICA","SHORT","","","","Identificador Caracteristica")
    arcpy.AddField_management(Elemento_Propiedad,"DA_VALOR","DATE","","","","Valor Fecha")
    arcpy.AddField_management(Elemento_Propiedad,"NU_VALOR","DOUBLE","","","","Valor Númerico")
    arcpy.AddField_management(Elemento_Propiedad,"VA_VALOR","TEXT","","","255","valor Texto")
    arcpy.AddField_management(Elemento_Propiedad,"FK_DOMINIO_CARACTERISTICA","SHORT","","","","Identificador dominio Caracteristica")
    arcpy.AddField_management(Elemento_Propiedad,"FECHA","DATE","","","","Fecha")

    arcpy.AddMessage("creando campos Tipo Muestra....")

    arcpy.AddField_management(Tipo_Muestra,"ID_TIPO_MUESTRA ","SHORT","","","","Identificador Tipo de Muestra")
    arcpy.AddField_management(Tipo_Muestra,"TIPO_MUESTRA","TEXT","","","50","Tipo de Muestra")

    arcpy.AddMessage("creando campos Caracteristica....")

    arcpy.AddField_management(Caracteristica,"ID_CARACTERISTICA","SHORT","","","","Identificador Caracteristica")
    arcpy.AddField_management(Caracteristica,"DESCRIPCION","TEXT","","","","Descripción")
    arcpy.AddField_management(Caracteristica,"FK_TIPO_MUESTRA","SHORT","","","","Tipo Muestra")
    arcpy.AddField_management(Caracteristica,"FK_PADRE_CARAC","SHORT","","","255","Caracteristica Padre")

    arcpy.AddMessage("creando campos Caracteristica Dominio....")

    arcpy.AddField_management(Caracteristica_Dominio,"ID_CARACTERISTICA","SHORT","","","","Identificador Caracteristica")
    arcpy.AddField_management(Caracteristica_Dominio,"DESCRIPCION","TEXT","","","","Descripción")
    arcpy.AddField_management(Caracteristica_Dominio,"FK_TIPO_MUESTRA","SHORT","","","","Tipo Muestra")

    arcpy.AddMessage("creando campos Pozo....")

    arcpy.AddField_management(Pozo,"ID_POZO","SHORT","","","","Identificador Pozo")
    arcpy.AddField_management(Pozo,"NOMBRE","TEXT","","","255","Nombre del Pozo")
    arcpy.AddField_management(Pozo,"X_ORIGINAL","DOUBLE","","","","Coordenadas X Originales")
    arcpy.AddField_management(Pozo,"Y_ORIGINAL","DOUBLE","","","","Coordenadas Y Originales")
    arcpy.AddField_management(Pozo,"Z_ORIGINAL","DOUBLE","","","","Coordenadas Z Originales")
    arcpy.AddField_management(Pozo,"PROFUNDIDAD","SHORT","","","","Profundidad")
    arcpy.AddField_management(Pozo,"FK_PROYECTO","SHORT","","","","Proyecto")
    arcpy.AddField_management(Pozo,"PROYECTO_CONTRATO","TEXT","","","50","Proyecto Contrato")
    arcpy.AddField_management(Pozo,"INCLINACION","DOUBLE","","","","Inclinación")
    arcpy.AddField_management(Pozo,"AZIMUTH","DOUBLE","","","","Azimuth")
    arcpy.AddField_management(Pozo,"OBSERVACIONES","TEXT","","","255","Observaciones")
    arcpy.AddField_management(Pozo,"RUTA_ENLACE","TEXT","","","255","Ruta Enlace")
    arcpy.AddField_management(Pozo,"DIST_TO","SHORT","","","","Distancia de")
    arcpy.AddField_management(Pozo,"FECHA_INICIO","DATE","","","","Fecha de Inicio")
    arcpy.AddField_management(Pozo,"FECHA_FIN","DATE","","","","Fecha Finalización")
    arcpy.AddField_management(Pozo,"DEPOSITO","LONG","","","","Deposito")
    arcpy.AddField_management(Pozo,"DIAMETRO","DOUBLE","","","","Diametro")
    arcpy.AddField_management(Pozo,"RESPONSABLE_CARGA","SHORT","","","","Descripción")
    arcpy.AddField_management(Pozo,"FK_PROPOSITO","SHORT","","","","Tipo Muestra")
    arcpy.AddField_management(Pozo,"RESPONSABLE_POZO","SHORT","","","","Identificador Caracteristica")
    arcpy.AddField_management(Pozo,"FK_TIPO_POZO","SHORT","","","","Descripción")
    arcpy.AddField_management(Pozo,"DIAMETRO_PERFORACION","DOUBLE","","","","Diametro Perforación")
    arcpy.AddField_management(Pozo,"DIAMETRO_REVESTIMIENTO","DOUBLE","","","","Diametro Revestimiento")
    arcpy.AddField_management(Pozo,"EQUIPO","TEXT","","","50","Equipo")
    arcpy.AddField_management(Pozo,"EMPRESA_CONTRATISTA","TEXT","","","255","Empresa Contratista")
    arcpy.AddField_management(Pozo,"RUTA_INFORME_PERFORACION","TEXT","","","255","Ruta Informe Perforación")
    arcpy.AddField_management(Pozo,"DIST_FROM","SHORT","","","","Distancia Hasta")
    arcpy.AddField_management(Pozo,"FK_DIST_UNIDAD","SHORT","","","","Unidad Distancia")
    arcpy.AddField_management(Pozo,"FK_TIPO_AZIMUTH","SHORT","","","","Tipo de Azimuth")
    arcpy.AddField_management(Pozo,"FK_TIPO_INCLINACION","SHORT","","","","Inclinación")

    arcpy.AddMessage("creando campos Detalle registro de Pozo....")


    arcpy.AddField_management(Detalle_Registro_Pozo,"ID_DETALLE","SHORT","","","","Identificador Detalle registro Pozo")
    arcpy.AddField_management(Detalle_Registro_Pozo,"FK_TIPO_REGISTRO","SHORT","","","","Tipo de Registro")
    arcpy.AddField_management(Detalle_Registro_Pozo,"FK_POZO","LONG","","","","Identificador Pozo")
    arcpy.AddField_management(Detalle_Registro_Pozo,"VALOR","DOUBLE","","","","Valor")
    arcpy.AddField_management(Detalle_Registro_Pozo,"PROFUNDIDAD_REGISTRO","SHORT","","","","Profundidad Registro")
    arcpy.AddField_management(Detalle_Registro_Pozo,"FROM","SHORT","","","","Desde")
    arcpy.AddField_management(Detalle_Registro_Pozo,"TO","SHORT","","","","Hasta")

    arcpy.AddMessage("creando campos Recovery....")

    arcpy.AddField_management(Recovery,"ID_RECOVERY","LONG","","","","Identificador Recovery")
    arcpy.AddField_management(Recovery,"POZO_ID_POZO","LONG","","","","Identificador Pozo_Pozo")
    arcpy.AddField_management(Recovery,"DIST_FROM","SHORT","","","","Distancia Desde")
    arcpy.AddField_management(Recovery,"DIST_TO","SHORT","","","","Distancia Hasta")
    arcpy.AddField_management(Recovery,"RECOVERY","DOUBLE","","","","Recovery")
    arcpy.AddField_management(Recovery,"RQD","DOUBLE","","","","RQD")
    arcpy.AddField_management(Recovery,"FK_FRECUENCIA_FRACTURAS","SHORT","","","","Frecuencia de Fracturas")
    arcpy.AddField_management(Recovery,"NUMERO_FRACTURAS","SHORT","","","","Número de fracturas")

    arcpy.AddMessage("creando campos Assay....")

    arcpy.AddField_management(Assay,"ID_ASSAY","SHORT","","","","Identificador Assay")
    arcpy.AddField_management(Assay,"FK_ID_MUESTRA","LONG","","","","Identificador Muestra")
    arcpy.AddField_management(Assay,"FK_COLLAR","LONG","","","","Identificador Collar")
    arcpy.AddField_management(Assay,"DIST_FROM","SHORT","","","","Distancia desde")
    arcpy.AddField_management(Assay,"DIST_TO","SHORT","","","","Distancia desde")
    arcpy.AddField_management(Assay,"ID_MANTO_CINTA","TEXT","","","2","Identificador Manto de Cinta")
    arcpy.AddField_management(Assay,"ESPESOR_VERDADERO","DOUBLE","","","","Espesor Verdadero")
    arcpy.AddField_management(Assay,"FK_MUESTRA","SHORT","","","","Muestra")
    arcpy.AddField_management(Assay,"FK_POZO","SHORT","","","","Pozo")

    arcpy.AddMessage("creando campos Estructura....")

    arcpy.AddField_management(Estructura,"ID_ESTRUCTURA_POZO","LONG","","","","Identificador Estructura Pozo")
    arcpy.AddField_management(Estructura,"DIST_FROM","DOUBLE","","","","Distancia Desde")
    arcpy.AddField_management(Estructura,"DIST_TO","DOUBLE","","","","Distancia Hasta")
    arcpy.AddField_management(Estructura,"LENGHT","SHORT","","","","Largo")
    arcpy.AddField_management(Estructura,"FK_TIPO_ESTRUCTURA","SHORT","","","","Tipo de Estructura")
    arcpy.AddField_management(Estructura,"INCLINACION_ESTRUCTURA","SHORT","","","","Inclinación Estructura")
    arcpy.AddField_management(Estructura,"TIPO_RELLENO","TEXT","","","255","tipo de Relleno")
    arcpy.AddField_management(Estructura,"APERTURA_ESTRUCTURA","SHORT","","","","Apertura Estructura")
    arcpy.AddField_management(Estructura,"FK_POZO","LONG","","","","Identificador Pozo")
    arcpy.AddField_management(Estructura,"DESCRIPCION","TEXT","","","255","Descripción")

    arcpy.AddMessage("Creando campos Litologia Pozo")

    arcpy.AddField_management(Litologia_Pozo,"ID_LOTOLOGIA_POZO","LONG","","","","Identificador Estructura Pozo")
    arcpy.AddField_management(Litologia_Pozo,"DIST_FROM","DOUBLE","","","","Distancia Desde")
    arcpy.AddField_management(Litologia_Pozo,"DIST_TO","DOUBLE","","","","Distancia Hasta")
    arcpy.AddField_management(Litologia_Pozo,"NOMBRE_ROCA_CAMPO","TEXT","","","255","Nombre Roca")
    arcpy.AddField_management(Litologia_Pozo,"DESCRIPCION","TEXT","","","255","Descripción")
    arcpy.AddField_management(Litologia_Pozo,"FK_TIPO_ROCA","SHORT","","","","Tipo de Roca")
    arcpy.AddField_management(Litologia_Pozo,"FK_POZO","LONG","","","","Indetificador Pozo")
    arcpy.AddField_management(Litologia_Pozo,"FK_COLOR","SHORT","","","","Color")
    arcpy.AddField_management(Litologia_Pozo,"INCLINACION_MUESTRA","SHORT","","","","Inclinación Muestra")
    arcpy.AddField_management(Litologia_Pozo,"BUZAMIENTO_REAL","SHORT","","","","Buzamiento")
    arcpy.AddField_management(Litologia_Pozo,"FK_UNIDAD_ESTRATIGRAFICA","SHORT","","","","Unidad Estatigráfica")


arcpy.CreateRelationshipClass_management(Muestra,Muestra_Laboratorio,Geodatabase+ os.sep+"Muestra_Resultado_Rel","SIMPLE","Atributos de Muestra","Atributos de Muestra Laboratorio","NONE","ONE_TO_MANY","NONE","ID_MUESTRA", "FK_ID_MUESTRA")
arcpy.CreateRelationshipClass_management(Muestra_Laboratorio,Resultado,Geodatabase+ os.sep+"Muestra_Laboratorio_Resultado_Rel","SIMPLE","Atributos de Muestra laboratorio","Atributos de Resultado","NONE","ONE_TO_MANY","NONE","ID_MUESTRA_LABORATORIO", "FK_MUESTRA_LABORATORIO")
arcpy.CreateRelationshipClass_management(Elemento_Propiedad,Resultado,Geodatabase+ os.sep+"Elemento_Propiedad_Resultado_Rel","SIMPLE","Atributos de Propiedad","Atributos de Resultado","NONE","ONE_TO_MANY","NONE","ID_ELEMENTO_PROPIEDAD", "FK_ELEMENTO_PROPIEDAD")
arcpy.CreateRelationshipClass_management(Elemento_Propiedad,Resultado,Geodatabase+ os.sep+"Elemento_Propiedad_Resultado_Rel","SIMPLE","Atributos de Propiedad","Atributos de Resultado","NONE","ONE_TO_MANY","NONE","ID_ELEMENTO_PROPIEDAD", "FK_ELEMENTO_PROPIEDAD")