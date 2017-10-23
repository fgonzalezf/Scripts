__author__ = 'fgonzalezf'

import arcpy, os, sys

GeodatabaseSalida=r"D:\MIIG\MIIG.mdb"
TablaDatos=r"D:\MIIG\MIIG.mdb\tabla2"
CampoIdentificador="IDENTIFICADOR_DEL_METADATO"
Salida= r"D:\MIIG\MIIG.mdb\METADATO_MIIG"
SalidaPol=r"D:\MIIG\MIIG.mdb\METADATO_MIIG_POL"

Borrar=True
Actualizar=True

def Campos(Feat,tipo,desc):
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    if tipo=="FeatureClass":
        if desc.shapeType=="Point":
            Lista.append('SHAPE@XY')
        else:
            Lista.append('SHAPE@')
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name.upper())
    return Lista

def ValoresSalida(Feat,fields):
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
def ValoresEntradaPunto(Feat,fields):
    datos = {}
    tindx=0
    indx = 0
    fields
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           X = 0
           Y = 0
           a = list(row)
           try:
               X= row[5]+ ((row[6]-row[5])/2)
               Y= row[7]+ ((row[8]-row[7])/2)
           except:
               X= 0
               Y= 0
           a.insert(0,(X,Y))
           row = tuple(a)
           datos[row[indx+1]] =row
    return datos

def ValoresEntradaPoligono(Feat,fields):
    datos = {}
    tindx=0
    indx = 0
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:

           lineArray = arcpy.Array()
           pnt1 = arcpy.Point(row[5],row[8])
           pnt2 = arcpy.Point(row[6],row[8])
           pnt3 = arcpy.Point(row[6],row[7])
           pnt4 = arcpy.Point(row[5],row[7])
           lineArray.add(pnt1)
           lineArray.add(pnt2)
           lineArray.add(pnt3)
           lineArray.add(pnt4)
           a = list(row)
           a.insert(0,arcpy.Polygon(lineArray))
           row = tuple(a)
           datos[row[indx+1]] =row
           lineArray.removeAll()
    return datos

def actualizarValores(Featin, FeatOut, fields,indx, valoresEntrada,valoresSalida):

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

                    keyvalue=row2[indx]
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
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fields)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            if keyvaluein not in valoresSalida:
                try:
                    #print len(valoresEntrada[keyvaluein])
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
                    keyvalue = row2[indx]
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

desc = arcpy.Describe(TablaDatos)
desc2 = arcpy.Describe(Salida)
desc3 = arcpy.Describe(SalidaPol)
tipo= desc.dataType
tipo2= desc2.dataType
tipo3= desc3.dataType
camposEntrada=Campos(TablaDatos,tipo,desc)
camposSalida=Campos(Salida,tipo2,desc2)
camposSalidaPol=Campos(SalidaPol,tipo3,desc3)



indx = camposSalida.index(CampoIdentificador.upper())

valoresEntrada=ValoresEntradaPunto(TablaDatos,camposEntrada)
valoresEntradaPol=ValoresEntradaPoligono(TablaDatos,camposEntrada)


valoresSalida=ValoresSalida(Salida,camposSalida)
valoresSalidaPol=ValoresSalida(SalidaPol,camposSalidaPol)

print camposEntrada
print camposSalida
print camposSalidaPol

actualizarValores(TablaDatos,Salida,camposSalida,indx,valoresEntrada,valoresSalida)

actualizarValores(TablaDatos,SalidaPol,camposSalidaPol,indx,valoresEntradaPol,valoresSalidaPol)