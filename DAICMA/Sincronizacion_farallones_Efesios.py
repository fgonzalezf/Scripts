import arcpy,os,sys

GeodatabaseSalida=r"E:\Scripts\EFESIOS.sde"


Capas = {}
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Area_Peligrosa"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Area_Peligrosa"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Area_Peligrosa_Punto"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Area_Peligrosa_Punto"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Areas_Canceladas"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Areas_Canceladas"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Areas_Canceladas_Punto"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Areas_Canceladas_Punto"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_No_Tecnicos"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_No_Tecnicos"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_No_Tecnicos_Punto"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_No_Tecnicos_Punto"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_Tecnicos"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_Tecnicos"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_Tecnicos_Punto"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Estudios_Tecnicos_Punto"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Eventos"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Eventos"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Sectores"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Sectores"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Zonas"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Zonas"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Municipios"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Municipios"
Capas[r"Z:\Pruebas_IMSMA\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Departamento"] =r"E:\Scripts\EFESIOS.sde\SDE.DBO.DAICMA\SDE.DBO.Departamento"



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

    camposentradaConj= set(camposEntrada)
    camposSalidaConj=set (camposSalida)
    iguales = camposSalidaConj & camposentradaConj
    normalizado= list(iguales)
    return normalizado

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

def actualizarValores(Featin, FeatOut, fieldsIn, fieldsOut,CampoUnico):
        indx=indexUnico(fieldsOut,CampoUnico)
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
                    keyvalue=row2[indx]
                    if keyvalue in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                print "Actualizando Valor..."+ row2[indx]+ "....("+str(Numerador)+ " de "+str(count)+")"
                                rowin =valoresEntrada[keyvalue]
                                cursor2.updateRow(rowin)
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error_actualizando"+ e.message

        edit.stopOperation()
        edit.stopEditing("True")
        Numerador = 0
        valoresSalida = ValoresEntrada(FeatOut,fieldsOut,indx)
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fieldsOut)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            if keyvaluein not in valoresSalida:
                try:
                    print "Ingresando Valor..." + str(keyvaluein)
                    rowin = valoresEntrada[keyvaluein]
                    print rowin
                    cursor3.insertRow(rowin)
                except  Exception as e:
                    print  "Error Ingresando ..."+ str(keyvaluein)+ "....(" + str(Numerador) + " de " + str(count) + ")"+ e.message
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
                                print "Borrando Valor..." + row2[indx] + "....(" + str(Numerador) + " de " + str(count) + ")"
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
for POLIGONO, PUNTOS in Capas.items():
    if os.path.basename(PUNTOS) == "SDE.DBO.Eventos":
        CampoUnico = "id_imsma_evento"
    elif os.path.basename(PUNTOS) == "SDE.DBO.Sectores":
        CampoUnico = "hazreduc_localid"
    elif os.path.basename(PUNTOS) == "SDE.DBO.Zonas":
        CampoUnico = "CODIGO_ZONA"
    elif os.path.basename(PUNTOS) == "SDE.DBO.Municipios":
        CampoUnico = "DANE"
    elif os.path.basename(PUNTOS) == "SDE.DBO.Departamento":
        CampoUnico = "COD_DEPART"
    else:
        CampoUnico = "FeatureID"
    print PUNTOS
    print CampoUnico
    FieldsIn=Campos(POLIGONO)
    FieldsOut=Campos(PUNTOS)
    listcampos=normalizarCampos(FieldsIn,FieldsOut)
    print "entrada: "+ str(POLIGONO)
    print "entrada: "+ str(listcampos)
    print "salida: "+ str(listcampos)
    actualizarValores(POLIGONO,PUNTOS,listcampos,listcampos,CampoUnico)