#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Actualización Geodatabase IMSMA a SDE Visores
# Author:      fgonzalezf
# Created:     03/03/2017
#-------------------------------------------------------------------------------

import arcpy, os, sys
GeodatabaseIMSMA=r"C:\Users\FernandoW7\Desktop\SIMMA\IMSMA.gdb"
GeodatabaseSDEImsma=r"C:\Users\FernandoW7\Desktop\SIMMA\Prueba_Final_1.gdb"

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
        valoresEntrada = ValoresEntrada(Featin,fields)
        Numerador=0
        result = arcpy.GetCount_management(Featin)
        count = int(result.getOutput(0))
        edit = arcpy.da.Editor (GeodatabaseSDEImsma)
        edit.startEditing ()
        edit.startOperation()
        if Actualizar == True:
            with arcpy.da.UpdateCursor(FeatOut, fields) as cursor2:
                for row2 in cursor2:
                    Numerador = Numerador + 1
                    keyvalue=row2[2]
                    if keyvalue in valoresEntrada:
                                print "Actualizando Valor..."+ row2[2]+ "....("+str(Numerador)+ " de "+str(count)+")"
                                cursor2.updateRow(valoresEntrada[keyvalue])

        edit.stopOperation()
        edit.stopEditing("True")
        Numerador = 0
        valoresSalida = ValoresEntrada(FeatOut,fields)
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fields)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            if keyvaluein not in valoresSalida:
                print "Ingresando Valor..." + keyvaluein + "....(" + str(Numerador) + " de " + str(count) + ")"
                cursor3.insertRow(valoresEntrada[keyvaluein])
        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida


                # Update the cursor with the updated list
arcpy.env.workspace=GeodatabaseIMSMA
ListaFeatEntrada= arcpy.ListFeatureClasses()

for fc in ListaFeatEntrada:
    FeatEntrada= GeodatabaseIMSMA+ os.sep+ fc
    FeatSalida= GeodatabaseSDEImsma+ os.sep+ "IMSMA"+ os.sep+fc
    listaF=ListaCampos(FeatEntrada)
    print fc
    actualizarValores(FeatEntrada,FeatSalida,listaF)

