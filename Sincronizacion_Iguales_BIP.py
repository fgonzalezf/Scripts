#!/usr/bin/python
# -*- coding: utf-8 -*-
import arcpy,os,sys

Entrada=r"C:\Users\Desarrollo\Documents\EPIS\epis.odc\.view_informes"
Salida=r'C:\Users\Desarrollo\Documents\EPIS\Tablas.gdb\T_view_informes'
GeodatabaseSalida=r'C:\Users\Desarrollo\Documents\EPIS\Tablas.gdb'

CampoIdentificador=""
arcpy.env.workspace=GeodatabaseSalida
desc = arcpy.Describe(Salida)
tipo= desc.dataType
print tipo

Actualizar=True
Borrar=True
indx = 0
def Campos(Feat):
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    if tipo=="FeatureClass":
        if desc.shapeType=="Point":
            Lista.append('SHAPE@XY')
        else:
            Lista.append('SHAPE@')
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name)
    return Lista

def ValoresEntrada(Feat,fields):
    datos = {}
    tindx=0
    indx = 0
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[indx]] =row
    return datos

def ValoresEntradaTotales(Feat,fields):
    datos = {}

    identificador=""

    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
            for field in fields:
                if row[fields.index(field)]== None:
                    identificador="None"+"_"
                else:
                    identificador=row[fields.index(field)]+"_"
            datos[identificador[:-1]] =row
    return datos

def actualizarValores(Featin, FeatOut, fields):
        valoresEntrada = ValoresEntradaTotales(Featin,fields)
        Numerador=0
        result = arcpy.GetCount_management(Featin)
        count = int(result.getOutput(0))
        edit = arcpy.da.Editor (GeodatabaseSalida)
        edit.startEditing ()
        edit.startOperation()
        if Actualizar == True:
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fields) as cursor2:
                for row2 in cursor2:
                    for field in fields:
                        if row2[fields.index(field)]== None:
                            identificadorOut="None"+"_"
                        else:
                            identificadorOut=row2[fields.index(field)]+"_"
                    keyvalue=identificadorOut[:-1]
                    if keyvalue in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Actualizando Valor..."+ str(row2[indx])+ "....("+str(Numerador)+ " de "+str(count)+")"
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
                    for field in fields:
                        if row2[fields.index(field)]== None:
                            identificadorOut="None"+"_"
                        else:
                            identificadorOut=row2[fields.index(field)]+"_"
                    keyvalue=identificadorOut[:-1]
                    if keyvalue not in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Borrando Valor..." + str(row2[indx]) + "....(" + str(Numerador) + " de " + str(count) + ")"
                                cursor2.deleteRow()
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..." + e.message

        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida
print Campos(Entrada)
Fields=Campos(Entrada)
actualizarValores(Entrada,Salida,Fields)
