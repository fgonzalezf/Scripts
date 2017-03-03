#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#-------------------------------------------------------------------------------
# Name:        Actualización de Puntos geograficos en base a Vista de tabla
# Purpose:
#
# Author:      fgonzalezf
#
# Created:     21/11/2014
# Copyright:   (c) fgonzalezf 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import sys
import os
import _winreg
from _winreg import *
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")
print "Proseso Iniciado................"
spMagna=arcpy.SpatialReference("MAGNA")
arcpy.env.workspace="Database Connections\METG_ODA_PROD.sde"
tabla = r"Database Connections\METG_ODA_PROD.sde\METG.V_CON_METADATA"
Puntos=r"Database Connections\METG_ODA_PROD.sde\METG.Metadato_Geografico\METG.METADATO"
#carpetaLogs=r"C:\Users\fgonzalezf\Documents\LogsActualizacionMetadatos"
workspace=r"Database Connections\METG_ODA_PROD.sde"
arcpy.Delete_management("in_memory/tableInMemory")
arcpy.Delete_management("LayerPuntos")
arcpy.Delete_management("layerApp")

expresion = "WESTBOUNDLONGITUDE IS NOT NULL AND EASTBOUNDLONGITUDE IS NOT NULL AND SOUTHBOUNDLATITUDE IS NOT NULL AND NORTHBOUNDLATITUDE IS NOT NULL"
expresion2= " AND ((EASTBOUNDLONGITUDE- WESTBOUNDLONGITUDE)/2)+ WESTBOUNDLONGITUDE > -82 AND ((EASTBOUNDLONGITUDE- WESTBOUNDLONGITUDE)/2)+ WESTBOUNDLONGITUDE < -66 AND  ((NORTHBOUNDLATITUDE- SOUTHBOUNDLATITUDE)/2)+ SOUTHBOUNDLATITUDE > -6 AND ((NORTHBOUNDLATITUDE- SOUTHBOUNDLATITUDE)/2)+ SOUTHBOUNDLATITUDE < 14 "
expresion= expresion+ expresion2
arcpy.TableSelect_analysis(tabla,"in_memory/tableInMemory",expresion )

#AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})

arcpy.AddField_management("in_memory/tableInMemory","NORTE","DOUBLE","","","","","NULLABLE")
arcpy.AddField_management("in_memory/tableInMemory","ESTE","DOUBLE","","","","","NULLABLE")
arcpy.AddField_management("in_memory/tableInMemory","URL","TEXT","","","255")
arcpy.AddField_management("in_memory/tableInMemory","EPOCA","TEXT","","","10")
arcpy.AddField_management("in_memory/tableInMemory","TEMATICA","TEXT","","","100")
arcpy.AddField_management("in_memory/tableInMemory","ESCALA","TEXT","","","20")

#CalculateField_management (in_table, field, expression, {expression_type}, {code_block})

expre_Norte= "((!NORTHBOUNDLATITUDE!- !SOUTHBOUNDLATITUDE!)/2)+ !SOUTHBOUNDLATITUDE!"
expre_Este= "((!EASTBOUNDLONGITUDE!- !WESTBOUNDLONGITUDE!)/2)+ !WESTBOUNDLONGITUDE!"
expre_Url= '"http://aplicaciones1.sgc.gov.co/sicat/html/SubProductos.aspx?Identificador="+ !FILEIDENTIFIER!'

code_blok1= """def Calcular (campo):
    valor=""
    if campo[:3]=="210" or campo[:3]=="220" or campo[:3]=="230" or campo[:3]=="240" or campo[:3]=="400":
        valor="2004"
    elif campo[:3]=="110" or campo[:3]=="120" or campo[:3]=="130" or campo[:3]=="140":
        valor = "1969"
    elif campo[:3]=="310" or campo[:3]=="320" or campo[:3]=="330" or campo[:3]=="340":
        valor = "1917"
    return valor"""
expre_anio= "Calcular( !FILEIDENTIFIER!)"

code_blok2= """def Calcular (campo):
    valor=""
    if campo[9:13]=="0005" :
        valor="1:5.000"
    elif  campo[9:13]=="0010":
        valor = "1:10.000"
    elif  campo[9:13]=="0025":
        valor = "1:25.000"
    elif  campo[9:13]=="0050":
        valor = "1:50.000"
    elif  campo[9:13]=="0100":
        valor = "1:100.000"
    elif  campo[9:13]=="0250":
        valor = "1:250.000"
    elif  campo[9:13]=="0500":
        valor = "1:500.000"
    elif  campo[9:13]=="0400":    
        valor = "1:400.000"
    elif campo[9:13]=="1000":
        valor = "1:1.000.000"
    elif campo[9:13]=="0000":
        valor= "SIN ESCALA"      
    return valor"""

expre_Escala="Calcular( !FILEIDENTIFIER!)"

code_block3= """def Calcular (campo):
    valor=""
    if campo[:5]=="21001" or campo[:5]=="11001"or campo[:5]=="31015":
        valor="Amenazas Geológicas: Sísmologia"
    elif  campo[:5]=="21002" or campo[:5]=="11002"or campo[:5]=="31014":
        valor = "Amenazas Geológicas: Vulcanología"
    elif  campo[:5]=="21003" or campo[:5]=="11003"or campo[:5]=="31013":
        valor = "Amenazas Geológicas: Movimientos en Masa"
    elif  campo[:5]=="21022" or campo[:5]=="11004"or campo[:5]=="31016":
        valor = "Amenazas Geológicas: Geomécanica"
    elif campo[:5]=="22004" or campo[:5]=="12005"or campo[:5]=="32001":
        valor = "Recursos del Subsuelo: Exploración y Evalución de Recursos Minerales"
    elif  campo[:5]=="22005" or campo[:5]=="12006"or campo[:5]=="32002":
        valor = "Recursos del Subsuelo: Hidrogeología"
    elif  campo[:5]=="22006" or campo[:5]=="12007":
        valor = "Recursos del Subsuelo: Geoquímica"
    elif  campo[:5]=="22007" or campo[:5]=="12008"or campo[:5]=="32003":
        valor = "Recursos del Subsuelo: Geofísica"
    elif  campo[:5]=="12009":
        valor = "Recursos del Subsuelo: Minerología"
    elif  campo[:5]=="23008" or campo[:5]=="13010"or campo[:5]=="33004":
        valor = "Geología Basica: Cartografía Geológica"
    elif  campo[:5]=="13011"or campo[:5]=="33005":
        valor = "Geología Basica: Geología Económica"
    elif  campo[:5]=="13012"or campo[:5]=="33006":
        valor = "Geología Basica: Geológia Regional"
    elif  campo[:5]=="13013"or campo[:5]=="33007":
        valor = "Geología Basica: Fotogeología"
    elif  campo[:5]=="13014"or campo[:5]=="33008":
        valor = "Geología Basica: Estratigrafía y Sedimentología"
    elif  campo[:5]=="13015"or campo[:5]=="33009":
        valor = "Geología Basica: Petrografía y Petrología"
    elif  campo[:5]=="13016"or campo[:5]=="33010":
        valor = "Geología Basica: Paleontología"
    elif  campo[:5]=="24009"or campo[:5]=="14017":
        valor = "Laboratorios: Minerales y Geoquímica"
    elif  campo[:5]=="24010"or campo[:5]=="14018":
        valor = "Laboratorios: Carbones"
    elif  campo[:5]=="24011"or campo[:5]=="14019":
        valor = "Laboratorios: Calibración Primaria"
    elif  campo[:5]=="24012"or campo[:5]=="14020":
        valor = "Laboratorios: Dosimetría Personal"
    elif  campo[:5]=="24013"or campo[:5]=="14021":
        valor = "Laboratorios: Reactor Nuclear"
    elif  campo[:5]=="14022"or campo[:5]=="34011":
        valor = "Laboratorios: Analisis Químico"
    elif  campo[:5]=="14023"or campo[:5]=="34012":
        valor = "Laboratorios: Química"
    elif  campo[:5]=="40014":
        valor = "Información: Información Georreferenciada"
    elif  campo[:5]=="40015":
        valor = "Información: Cartografía Básica IGAC"
    elif  campo[:5]=="40016":
        valor = "Información: Cartografía Básica DANE"
    elif  campo[:5]=="40017":
        valor = "Información: Cartografía Basica INGEOMINAS"
    elif  campo[:5]=="40018":
        valor = "Información: Fotografías Aéreas"
    elif  campo[:5]=="40019":
        valor = "Información: Sensores Remotos"
    elif  campo[:5]=="40020":
        valor = "Información: Modelo Digital de Elevación"
    elif  campo[:5]=="15618":
        valor = "Participación Ciudadana: Referencia"
    return valor"""

expre_Tematica="Calcular( !FILEIDENTIFIER!)"


arcpy.CalculateField_management("in_memory/tableInMemory","NORTE",expre_Norte,"PYTHON")
arcpy.CalculateField_management("in_memory/tableInMemory","ESTE",expre_Este,"PYTHON")
arcpy.CalculateField_management("in_memory/tableInMemory","URL",expre_Url,"PYTHON")
arcpy.CalculateField_management("in_memory/tableInMemory","EPOCA",expre_anio,"PYTHON",code_blok1)
arcpy.CalculateField_management("in_memory/tableInMemory","TEMATICA",expre_Tematica,"PYTHON",code_block3)
arcpy.CalculateField_management("in_memory/tableInMemory","ESCALA",expre_Escala,"PYTHON",code_blok2)

#Acceder a la Carpeta mis documentos
aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
aKey = OpenKey(aReg, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
t=QueryValueEx(aKey,"Personal")
pathMisDocumentos = t[-2]
CloseKey(aKey)
CloseKey(aReg)
try:
    pathlogs= os.mkdir ( pathMisDocumentos+r"\LogsActualizacion")
    print(pathlogs)
except:
    pathlogs=pathMisDocumentos+r"\LogsActualizacion"
    pass

ahora = datetime.datetime.now()
NombreArchivo =str(ahora.year)+str(ahora.month) +str(ahora.day) + str(ahora.hour) +str(ahora.minute)+str(ahora.second)+".txt"
Fileprj = open(pathlogs + os.sep+ NombreArchivo, "w")

layer=arcpy.MakeXYEventLayer_management("in_memory/tableInMemory", "ESTE", "NORTE", "LayerPuntos", spMagna)
fields = ["MD_METADATA_ID","FILEIDENTIFIER","TITLE","CI_DATE_ID","REFDATE","MD_IDENTIFICATION_ID","DENOMINATOR","WESTBOUNDLONGITUDE","EASTBOUNDLONGITUDE","SOUTHBOUNDLATITUDE","NORTHBOUNDLATITUDE","NORTE","ESTE","URL","EPOCA","TEMATICA","ESCALA","SHAPE@XY"]
Y=0
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()
print "Actualizando..........."
with arcpy.da.UpdateCursor("LayerPuntos", fields) as cursor1:
    for row1 in cursor1:      
        Y=Y+1
        print "Registro... " + str(Y)
        rowexpresion= "MD_METADATA_ID ="+str(row1[0])
        with arcpy.da.UpdateCursor(Puntos, fields ,rowexpresion) as cursor2:
            X=0
            
            for row2 in cursor2:
                X=X+1
                #print X
                try:
                    if row2[0]== row1[0]:

                        row2[1]=str(row1[1]).encode('iso-8859-1')
                        row2[2]=str(row1[2]).encode('iso-8859-1')
                        row2[3]=row1[3]if row1[3] else None
                        row2[4]=row1[4]if row1[4] else None
                        row2[5]=row1[5]
                        row2[6]=row1[6]
                        row2[7]=row1[7]
                        row2[8]=row1[8]
                        row2[9]=row1[9]
                        row2[10]=row1[10]
                        row2[11]=row1[11]
                        row2[12]=row1[12]
                        row2[13]=row1[13]
                        row2[14]=row1[14]
                        row2[15]=row1[15]
                        row2[16]=row1[16]
                        row2[17]=row1[17]
                        cursor2.updateRow(row2)
                        Fileprj.write("Registro Actualizado: " + rowexpresion + "\n")
                except Exception as e:
                    print e.message
                    Fileprj.write("Error Actualizado: " + rowexpresion + " :" + e.message +"\n")
                    pass
               
            if X==0:
                    try:
                        print "insertando puntos"
                        #Insercion de Puntos Nuevos
                        #arcpy.MakeFeatureLayer_management("LayerPuntos","layerApp",rowexpresion)
                        #arcpy.Append_management("layerApp",Puntos,"NO_TEST")
                        #arcpy.Delete_management("layerApp")
                        cursor3 = arcpy.da.InsertCursor(Puntos,fields)
                        cursor3.insertRow(row1)
                        del cursor3
                        Fileprj.write("Registro Ingresado: " + rowexpresion + "\n")
                    except Exception as e:
                        print e.message
                        print "Error en Insertando:  " + rowexpresion
                        #arcpy.Delete_management("layerApp")
                        Fileprj.write("Error ingresando Ingresado: " + rowexpresion  + " :" + e.message+ "\n")
                        pass


#Borrado de registros
print "Borrado de registros............"
Y=0
with arcpy.da.UpdateCursor(Puntos, fields) as cursor1:
    for row1 in cursor1:
        Y=Y+1
        print "Registro... " + str(Y)
        rowexpresion= "MD_METADATA_ID ="+str(row1[0])
        with arcpy.da.UpdateCursor("LayerPuntos", fields ,rowexpresion) as cursor2:
            X=0
            #print X
            for row2 in cursor2:
                X=X+1
            if X==0:
                try:
                    arcpy.MakeFeatureLayer_management(Puntos,"layerApp2",rowexpresion)
                    arcpy.DeleteFeatures_management("layerApp2")
                    arcpy.Delete_management("layerApp2")
                    Fileprj.write("Registro Borrado: " + rowexpresion + "\n")
                except Exception as e:
                    print e.message
                    print "Error en Borrando:  " + rowexpresion
                    arcpy.Delete_management("layerApp2")
                    Fileprj.write("Error Borrando Registro: " + rowexpresion  + " :" + e.message+ "\n")
                    pass
edit.stopOperation()
edit.stopEditing(True)
arcpy.Delete_management("in_memory/tableInMemory")
arcpy.Delete_management("LayerPuntos")
Fileprj.close()
