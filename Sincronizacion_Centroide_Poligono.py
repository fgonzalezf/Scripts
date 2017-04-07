import arcpy,os,sys

EntradaPol=r"D:\APN\BK_05_04_2017.mdb\Hazard_AP_APC_Polygons_I_Visor"
SalidaPun=r"D:\APN\BK_05_04_2017.mdb\DAICMA\Area_Peligrosa_Punto"
GeodatabaseSalida=r"D:\APN\BK_05_04_2017.mdb"
desc = arcpy.Describe(EntradaPol)
tipo= desc.dataType
print tipo
Actualizar=True
Borrar=True

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
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[3]] =row
    return datos

def actualizarValores(Featin, FeatOut, fieldsIn, fieldsOut):
        valoresEntrada = ValoresEntrada(Featin,fieldsIn)
        Numerador=0
        result = arcpy.GetCount_management(Featin)
        count = int(result.getOutput(0))
        edit = arcpy.da.Editor (GeodatabaseSalida)
        edit.startEditing ()
        edit.startOperation()
        if Actualizar == True:
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fieldsOut) as cursor2:
                for row2 in cursor2:
                    keyvalue=row2[3]
                    if keyvalue in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Actualizando Valor..."+ row2[3]+ "....("+str(Numerador)+ " de "+str(count)+")"
                                rowin =valoresEntrada[keyvalue]
                                rowin = list(rowin)
                                pointCentroid= rowin[0].trueCentroid
                                del rowin[0]
                                rowin.insert(0,pointCentroid)
                                rowin = tuple(rowin)
                                print rowin
                                cursor2.updateRow(rowin)
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..."+ e.message

        edit.stopOperation()
        edit.stopEditing("True")
        Numerador = 0
        valoresSalida = ValoresEntrada(FeatOut,fieldsOut)
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fieldsOut)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            if keyvaluein not in valoresSalida:
                try:
                    print "Ingresando Valor..." + keyvaluein + "....(" + str(Numerador) + " de " + str(count) + ")"
                    rowin = valoresEntrada[keyvaluein]
                    rowin=list(rowin)
                    pointCentroid = rowin[0].trueCentroid
                    del rowin[0]
                    rowin.insert(0, pointCentroid)
                    rowin=tuple(rowin)
                    print rowin
                    cursor3.insertRow(rowin)
                except  Exception as e:
                    print  "Error... "+ e.message
        edit.stopOperation()
        edit.stopEditing("True")

        edit.startEditing()
        edit.startOperation()
        if Borrar == True:
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fieldsOut) as cursor2:
                for row2 in cursor2:
                    keyvalue = row2[3]
                    if keyvalue not in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Borrando Valor..." + row2[3] + "....(" + str(Numerador) + " de " + str(count) + ")"
                                cursor2.deleteRow()
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..." + e.message

        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida
print Campos(EntradaPol)
FieldsIn=Campos(EntradaPol)
FieldsOut=Campos(SalidaPun)
print "entrada: "+ str(FieldsIn)
print "salida: "+ str(FieldsOut)
actualizarValores(EntradaPol,SalidaPun,FieldsIn,FieldsOut)
