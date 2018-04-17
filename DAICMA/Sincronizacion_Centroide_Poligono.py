import arcpy,os,sys



GeodatabaseSalida=r"Z:\Pruebas_IMSMA\SDE.sde"
CampoUnico="FeatureID"

Capas = {}
Capas[r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Area_Peligrosa"] =r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Area_Peligrosa_Punto"
Capas[r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Areas_Canceladas"] =r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Areas_Canceladas_Punto"
Capas[r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_No_Tecnicos"] =r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_No_Tecnicos_Punto"
Capas[r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_Tecnicos"] =r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_Tecnicos_Punto"


Actualizar=True
Borrar=True

def Campos(Feat):
    desc = arcpy.Describe(Feat)
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    if desc.dataType=="FeatureClass":
        print desc.shapeType
        if desc.shapeType=="Point":
            Lista.append('SHAPE@XY')
        else:
            Lista.append('SHAPE@')
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name)
    return Lista

def normalizarCampos(camposEntrada, camposSalida):
    campos=[]
    entrada=set(camposEntrada)
    salida=set(camposSalida)
    inter=entrada.intersection(salida)
    entrada=list(inter)
    salida=list(inter)
    entrada.insert(0, "SHAPE@")
    salida.insert(0, "SHAPE@XY")
    campos.append(entrada)
    campos.append(salida)
    return campos

def indexUnico(CamposEntradaind,index):
    x=0
    for campo in CamposEntradaind:
        if campo == index:
            return x
        x=x+1

def ValoresEntrada(Feat,fields,indexEnt):
    datos = {}
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[indexEnt]] =row
    return datos

def actualizarValores(Featin, FeatOut, fieldsIn, fieldsOut):
        indx=indexUnico(fieldsIn,CampoUnico)
        indxOut=indexUnico(fieldsOut,CampoUnico)
        valoresEntrada = ValoresEntrada(Featin,fieldsIn,indx)
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
                    keyvalue=row2[indxOut]
                    if keyvalue in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Actualizando Valor..."+ keyvalue+ str(count)
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
                                print "Error..."+ e.message+("1")

        edit.stopOperation()
        edit.stopEditing("True")
        Numerador = 0
        valoresSalida = ValoresEntrada(FeatOut,fieldsOut,indxOut)
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fieldsOut)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            if keyvaluein not in valoresSalida:
                try:
                    print "Ingresando Valor..." + keyvaluein + str(count)
                    rowin = valoresEntrada[keyvaluein]
                    rowin=list(rowin)
                    pointCentroid = rowin[0].trueCentroid
                    del rowin[0]
                    rowin.insert(0, pointCentroid)
                    rowin=tuple(rowin)
                    print rowin
                    cursor3.insertRow(rowin)
                except  Exception as e:
                    print  "Error... "+ e.message+("2")
        edit.stopOperation()
        edit.stopEditing("True")

        edit.startEditing()
        edit.startOperation()
        if Borrar == True:
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fieldsOut) as cursor2:
                for row2 in cursor2:
                    keyvalue = row2[indx]
                    if keyvalue not in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Borrando Valor..." + row2[indx] +  str(count) 
                                cursor2.deleteRow()
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..." + e.message+("3")

        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida
#print Campos(EntradaPol)
for POLIGONO, PUNTOS in Capas.items():
    FieldsIn=Campos(POLIGONO)
    FieldsOut=Campos(PUNTOS)
    nuevos=normalizarCampos(FieldsIn,FieldsOut)
    FieldsIn=nuevos[0]
    FieldsOut=nuevos[1]
    print FieldsIn
    print FieldsOut
    print "capa "+ str(POLIGONO)
    
    actualizarValores(POLIGONO,PUNTOS,nuevos[0],nuevos[1])
