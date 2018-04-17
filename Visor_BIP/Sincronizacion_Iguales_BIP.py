#!/usr/bin/python
# -*- coding: utf-8 -*-
import arcpy,os,sys
import mysql.connector


Actualizar=True
Borrar=True
indx = 0



def listFieldsMySQL(tabla):
    cnx = mysql.connector.connect(user='gaudi_arcgis',database='sgv',password='Arcgis_2017',host='172.25.3.88')
    cursor = cnx.cursor()
    query = ("DESCRIBE " + tabla )
    cursor.execute(query)
    listaFields=[]
    for row in cursor:
      listaFields.append(row[0])
    cnx.close()
    return listaFields


def ValoresEntrada(Feat,fields):
    cnx = mysql.connector.connect(user='gaudi_arcgis',database='sgv',password='Arcgis_2017',host='172.25.3.88')
    datos = {}
    tindx=0
    indx = 0
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    cursor = cnx.cursor()
    query = ("SELECT * FROM " + Feat)
    cursor.execute(query)
    listaFields=[]
    for row in cursor:
        datos[row[indx]] =row
    cnx.close()
    return datos

def ValoresEntradaTotales(Feat,fields):
    cnx = mysql.connector.connect(user='gaudi_arcgis',database='sgv',password='Arcgis_2017',host='172.25.3.88')
    datos = {}

    identificador=""
    cursor = cnx.cursor()
    query = ("SELECT * FROM " + Feat)
    cursor.execute(query)
    for row in cursor:
        identificador=""
        for field in fields:
            if row[fields.index(field)]== None:
                identificador=identificador+"_"+"None"
            else:
                identificador=identificador+"_"+row[fields.index(field)]
            datos[identificador]=row
    cnx.close()
    return datos
def CountMysql(tabla):
    cnx = mysql.connector.connect(user='gaudi_arcgis', database='sgv',password='Arcgis_2017',host='172.25.3.88')
    cursor = cnx.cursor()
    query ="select count(*) from "+ tabla
    #query = ("DESCRIBE " + tabla )
    cursor.execute(query)
    count=0
    for row in cursor:
       count=row[0]
    return count
def actualizarValores(Featin, FeatOut, fields):
        valoresEntrada = ValoresEntradaTotales(Featin,fields)
        Numerador=0
        count = CountMysql(Featin)
        edit = arcpy.da.Editor (GeodatabaseSalida)
        edit.startEditing ()
        edit.startOperation()
        if Actualizar == True:
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fields) as cursor2:
                for row2 in cursor2:
                    identificadorOut=""
                    for field in fields:
                        if row2[fields.index(field)]== None:
                            identificadorOut=identificadorOut+"_"+"None"
                        else:
                            identificadorOut=identificadorOut+"_"+row2[fields.index(field)]
                    keyvalue=identificadorOut
                    if keyvalue in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Actualizando Valor..."+ str(keyvalue)+ "....("+str(Numerador)+ " de "+str(count)+")"
                                cursor2.updateRow(valoresEntrada[keyvalue])
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..."+ e.message


        edit.stopOperation()
        edit.stopEditing("True")
        Numerador = 0
        valoresSalida = ValoresEntradaTotales(FeatOut,fields)
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fields)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            if keyvaluein not in valoresSalida:
                try:
                    print "Ingresando Valor..." + str(keyvaluein) + "....(" + str(Numerador) + " de " + str(count) + ")"
                    cursor3.insertRow(valoresEntrada[keyvaluein])
                except  Exception as e:
                    print  "Error... "+ e.message
        edit.stopOperation()
        edit.stopEditing("True")

        edit.startEditing()
        edit.startOperation()
        if Borrar == True:
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fields) as cursor2:
                for row2 in cursor2:
                    identificadorOut=""
                    for field in fields:
                        if row2[fields.index(field)]== None:
                            identificadorOut=identificadorOut+"_"+"None"
                        else:
                            identificadorOut=identificadorOut+"_"+row2[fields.index(field)]
                    keyvalue=identificadorOut
                    if keyvalue not in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Borrando Valor..." + str(keyvalue) + "....(" + str(Numerador) + " de " + str(count) + ")"
                                cursor2.deleteRow()
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..." + e.message

        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida

Tablas=[]

Tablas.append(["view_informes",r'C:/temp/EPISODAPROD.sde/EPIS.T_view_informes',r'C:/temp/EPISODAPROD.sde'])
Tablas.append(["view_contratos",r'C:/temp/EPISODAPROD.sde/EPIS.T_view_contratos',r'C:/temp/EPISODAPROD.sde'])
Tablas.append(["view_pozos",r'C:/temp/EPISODAPROD.sde/EPIS.T_view_pozos',r'C:/temp/EPISODAPROD.sde'])
Tablas.append(["view_sismica2d",r'C:/temp/EPISODAPROD.sde/EPIS.T_view_sismica2d',r'C:/temp/EPISODAPROD.sde'])
Tablas.append(["view_sismica3d",r'C:/temp/EPISODAPROD.sde/EPIS.T_view_sismica3d',r'C:/temp/EPISODAPROD.sde'])


for tabla in Tablas:
    Entrada=tabla[0]
    Salida=tabla[1]
    GeodatabaseSalida=tabla[2]
    print GeodatabaseSalida

    CampoIdentificador=""

    Fields=listFieldsMySQL(Entrada)
    actualizarValores(Entrada,Salida,Fields)
