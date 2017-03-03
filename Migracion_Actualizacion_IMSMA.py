#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Actualización Geodatabase IMSMA a SDE Visores
# Author:      fgonzalezf
# Created:     03/03/2017
#-------------------------------------------------------------------------------

import arcpy, os, sys
GeodatabaseIMSMA=r"D:\APN\Pruebas_Cargue_IMSMA\IMSMA.gdb"
GeodatabaseSDEImsma=r"D:\APN\Pruebas_Cargue_IMSMA\PRUEBACARGUE.gdb"

#Configuracion
Actualizar=True
Insertar=True

fcprueba= GeodatabaseIMSMA+ os.sep+ "Hazard_Reductions_polygon"
fcpruebasalida=GeodatabaseSDEImsma+os.sep+"Hazard_Reductions_polygon"
def ListaCampos(Feat):
    ListaFinal=[]
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.editable==True and field.type!="Geometry" and field.type!="OID":
            ListaFinal.append(field.name)
    Des= arcpy.Describe(Feat)
    if Des.shapeType=="Point":
        ListaFinal.append('SHAPE@XY')
    else:
        ListaFinal.append('SHAPE@')
    return ListaFinal

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[2] for row in cursor})

def ValoresEntrada(Feat,fields):
    datos = {}
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[2]] =row
    return datos

def actualizarValores(Featin, FeatOut, fields):
        valores = ValoresEntrada(Featin,fields)
        Numerador=0
        result = arcpy.GetCount_management(Featin)
        count = int(result.getOutput(0))
        expresion=arcpy.AddFieldDelimiters(GeodatabaseIMSMA,fields[2])
        edit = arcpy.da.Editor (GeodatabaseSDEImsma)
        edit.startEditing ()
        edit.startOperation()
        for id, row in valores.items():
            query= expresion+"='"+row[2]+"'"
            estado=False
            Numerador=Numerador+1
            with arcpy.da.UpdateCursor(FeatOut, fields, query) as cursor2:
                for row2 in cursor2:
                    estado=True
                    if Actualizar==True:
                        print "Actualizando Valor..."+ row[2]+ "....("+str(Numerador)+ " de "+str(count)+")"
                        if row[2]==row2[2]:
                            for i in range(len(row)):
                                row2[i]=row[i]
                        cursor2.updateRow(row2)
            if estado==False:
                if Insertar==True:
                    print "Ingresando Valor Nuevo..."+ row[2]+ "....("+str(Numerador)+" de "+str(count)+")"
                    cursor3 = arcpy.da.InsertCursor(FeatOut, fields)
                    cursor3.insertRow(row)
        edit.stopOperation()
        edit.stopEditing("True")
            # Update the cursor with the updated list
arcpy.env.workspace=GeodatabaseIMSMA
ListaFeatEntrada= arcpy.ListFeatureClasses()

for fc in ListaFeatEntrada:
    FeatEntrada= GeodatabaseIMSMA+ os.sep+ fc
    FeatSalida= GeodatabaseSDEImsma+ os.sep+ "IMSMA"+ os.sep+fc
    listaF=ListaCampos(FeatEntrada)
    print fc
    actualizarValores(FeatEntrada,FeatSalida,listaF)


