import arcpy,os,sys

EntradaPol=r"D:\APN\BK_Prueba.gdb\daicmatbl_hazard_Eventos"
SalidaPun=r"D:\APN\BK_Prueba.gdb\DAICMA\Eventos"
GeodatabaseSalida=r"D:\APN\BK_Prueba.gdb"
CampoUnico="id_imsma_evento"


Actualizar=True
Borrar=True
sr = arcpy.SpatialReference(4326)

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

    for fieldEnt in camposEntrada:
        if fieldEnt != 'SHAPE@' and fieldEnt != 'SHAPE@XY'and fieldEnt != 'TEMP':
            if fieldEnt not in camposSalida:
                camposEntrada.remove(fieldEnt)
    for fieldSal in camposSalida:
        if fieldSal != 'SHAPE@' and fieldSal != 'SHAPE@XY':
            if fieldSal not in camposEntrada:
                camposSalida.remove(fieldSal)

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
        indxOut=indexUnico(fieldsOut,CampoUnico)
        indxIn=indexUnico(fieldsIn,CampoUnico)
        indxLogX=indexUnico(fieldsOut,"longitude")
        indxLatY=indexUnico(fieldsOut,"latitude")
        valoresEntrada = ValoresEntrada(Featin,fieldsIn,indxIn)
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
                                print "Actualizando Valor..."+ row2[indxOut]+ "....("+str(Numerador)+ " de "+str(count)+")"
                                rowin =valoresEntrada[keyvalue]
                                rowin = list(rowin)
                                pointCentroid= arcpy.Point(0,0)
                                pointCentroid.X =float(rowin[indxLogX])
                                pointCentroid.Y = float(rowin[indxLatY])
                                #del rowin[0]
                                ptGeometry = arcpy.PointGeometry(pointCentroid,sr)

                                rowin.insert(0,ptGeometry)
                                rowin = tuple(rowin)
                                print rowin
                                cursor2.updateRow(rowin)
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..."+ e.message

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
                    print "Ingresando Valor..." + keyvaluein + "....(" + str(Numerador) + " de " + str(count) + ")"
                    rowin = valoresEntrada[keyvaluein]
                    rowin=list(rowin)
                    pointCentroid = arcpy.Point(0, 0)
                    pointCentroid.X = float(rowin[indxLogX])
                    pointCentroid.Y = float(rowin[indxLatY])
                    # del rowin[0]
                    ptGeometry = arcpy.PointGeometry(pointCentroid, sr)

                    rowin.insert(0, ptGeometry)
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
                    keyvalue = row2[indxOut]
                    if keyvalue not in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Borrando Valor..." + row2[indxOut] + "....(" + str(Numerador) + " de " + str(count) + ")"
                                cursor2.deleteRow()
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..." + e.message

        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida
#print Campos(EntradaPol)
FieldsIn=Campos(EntradaPol)
FieldsOut=Campos(SalidaPun)
normalizarCampos(FieldsIn,FieldsOut)
print "entrada: "+ str(FieldsIn)
print "salida: "+ str(FieldsOut)
actualizarValores(EntradaPol,SalidaPun,FieldsIn,FieldsOut)