# -*- coding: utf-8 -*-
import arcpy,os,sys,re, os,datetime,shutil
import xlrd as xl

#ExcelEntrada =arcpy.GetParameterAsText(0)
#Actualizar=arcpy.GetParameterAsText(1)
#GeodatabaseSalida=r"E:\Scripts\SDE.sde"

ExcelEntrada =arcpy.GetParameterAsText(0)
Actualizar=arcpy.GetParameterAsText(1)
GeodatabaseSalida=r"E:\Scripts\SDE.sde"
carpetaNueva= r"E:\Reportes_CENAM_Excel\Excel"

arcpy.env.overwriteOutput=True

CampoUnico="ID"

def maximoId(FeatIn):
    idmax=0
    with arcpy.da.SearchCursor(FeatIn, "ID") as cursor:
        for row in cursor:
            if idmax <= row[0]:
                idmax=row[0]
    return idmax

def convertDecimal(textoSexagesimal):
    decimal = 0.0
    temp=""
    if isinstance(textoSexagesimal, float):
        decimal= textoSexagesimal
    else:
        for y in textoSexagesimal:

            if (y in ['0','1','2','3','4','5','6','7','8','9'," ","N","W"]):
                temp=temp+y
        Numeros=temp.split(" ")

        if Numeros[3]=="N":
            decimal = float(Numeros[0])+float(Numeros[1])/60+float(Numeros[2])/3600
        else:
            decimal = (-1)*float(Numeros[0]) - float(Numeros[1]) / 60 -float(Numeros[2]) / 3600

    return float(decimal)

def copiarRenombrar(rutaVieja, carpeta):
    carpetaNueva = carpeta
    fechaHoy =datetime.datetime.now()
    strFecha=fechaHoy.strftime('%Y%m%d%H%M%S')
    shutil.copy(rutaVieja,carpetaNueva)
    os.rename(carpetaNueva+os.sep+os.path.basename(rutaVieja), carpetaNueva+os.sep+strFecha+".xlsx")
    print strFecha
    return carpetaNueva+os.sep+strFecha+".xlsx"

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def getSheetName(file_name):
    pointSheetObj = []
    TeamPointWorkbook = xl.open_workbook(file_name)
    pointSheets = TeamPointWorkbook.sheet_names()
    return pointSheets
arcpy.AddMessage("Iniciando Migracion ...")

ExcelEntrada=copiarRenombrar(ExcelEntrada,carpetaNueva)
ListaHojas = getSheetName(ExcelEntrada)
Tablas=[]
for hoja in ListaHojas:
    tablatemp=[]
    if hoja == "Operaciones" or hoja == "Accidentes":
        arcpy.ExcelToTable_conversion(ExcelEntrada,"in_memory"+os.sep+hoja+"tabla",hoja)
        tablatemp.append("in_memory"+os.sep+hoja+"tabla")
        tablatemp.append(GeodatabaseSalida + os.sep + "CENAM"+ os.sep+ hoja )
        tablatemp.append(GeodatabaseSalida )
        Tablas.append(tablatemp)

Borrar=False

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
        if fld.editable==True and fld.type!="Geometry" and fld.name!="RESUMEN_DE_LOS_HECHOS":
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
        indxLogX=indexUnico(fieldsIn,"Latitud_decimales")
        indxLatY=indexUnico(fieldsIn,"Longitud_decimales")


        indxdiain=fieldsIn.index("DIA__DD_")
        indxmesin=fieldsIn.index("MES__MM_")
        indxanioin = fieldsIn.index( u'A\xd1O__AAAA_')
        indxdepin = fieldsIn.index("DEPARTAMENTO")
        indxmunin = fieldsIn.index("MUNICIPIO")
        indxIdin = fieldsIn.index("ID")
        IDmax= maximoId(FeatOut)
        try:
            indxnomin = fieldsIn.index("NOMBRES_APELLIDOS")
        except:
            indxnomin = None



        indxfechaout=indexUnico(fieldsIn, "FECHA___DD_MM_AAAA_")

        valoresEntrada = ValoresEntrada(Featin,fieldsIn,indxIn)
        Numerador=0
        result = arcpy.GetCount_management(Featin)
        count = int(result.getOutput(0))
        edit = arcpy.da.Editor (GeodatabaseSalida)
        edit.startEditing ()
        edit.startOperation()
        if Actualizar == "true":
            Controlvalores = []
            with arcpy.da.UpdateCursor(FeatOut, fieldsOut) as cursor2:
                for row2 in cursor2:
                    keyvalue=row2[indxOut]
                    if keyvalue in valoresEntrada:
                        if keyvalue not in Controlvalores:
                            try:
                                Numerador = Numerador + 1
                                arcpy.AddMessage( "Actualizando Valor..."+ str(row2[indxOut])+ "....("+str(Numerador)+ " de "+str(count)+")")
                                rowin =valoresEntrada[keyvalue]
                                rowin = list(rowin)
                                rowin[indxdiain] = datetime.datetime(rowin[indxanioin], rowin[indxmesin],
                                                                     rowin[indxdiain])

                                rowin[indxdepin] = rowin[indxdepin] + "-" + rowin[indxmunin]
                                if indxnomin != None:
                                    rowin.insert(indxnomin, "")
                                pointCentroid = arcpy.Point(convertDecimal(rowin[indxLogX]),
                                                            convertDecimal(rowin[indxLatY]))
                                rowin[indxLogX] = convertDecimal(rowin[indxLogX])
                                rowin[indxLatY] = convertDecimal(rowin[indxLatY])
                                rowin.pop(indxmesin)
                                rowin.pop(indxanioin - 1)
                                rowin.pop(indxmunin - 2)
                                # del rowin[0]
                                rowin.insert(0, pointCentroid)


                                #del rowin[0]

                                rowin = tuple(rowin)
                                #print rowin
                                cursor2.updateRow(rowin)
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                arcpy.AddMessage( "Error..."+ e.message)

        edit.stopOperation()
        edit.stopEditing("True")
        Numerador = 0
        valoresSalida = ValoresEntrada(FeatOut,fieldsOut,indxOut)
        edit.startEditing()
        edit.startOperation()
        cursor3 = arcpy.da.InsertCursor(FeatOut, fieldsOut)
        for keyvaluein in valoresEntrada:
            Numerador= Numerador+1
            IDmax =IDmax+1
            if Actualizar == "false":
                #try:
                        arcpy.AddMessage( "Ingresando Valor..." + str(keyvaluein) + "....(" + str(Numerador) + " de " + str(count) + ")")
                        rowin = valoresEntrada[keyvaluein]
                        rowin=list(rowin)

                        rowin[indxdiain] = datetime.datetime(rowin[indxanioin], rowin[indxmesin], rowin[indxdiain])

                        rowin[indxdepin] = rowin[indxdepin] + "-" + rowin[indxmunin]
                        if indxnomin != None:
                            rowin.insert(indxnomin, "")
                        pointCentroid= arcpy.Point(convertDecimal(rowin[indxLogX]), convertDecimal(rowin[indxLatY]))
                        rowin[indxLogX]=convertDecimal(rowin[indxLogX])
                        rowin[indxLatY]=convertDecimal(rowin[indxLatY])
                        rowin[indxIdin] =IDmax
                        rowin.pop(indxmesin)
                        rowin.pop(indxanioin-1)
                        rowin.pop(indxmunin-2)
                        #del rowin[0]
                        rowin.insert(0, pointCentroid)
                        rowin=tuple(rowin)
                        print rowin
                        cursor3.insertRow(rowin)
                #except  Exception as e:
            #arcpy.AddMessage(  "Error3... "+ e.message)
            elif Actualizar == "true":
                if keyvaluein not in valoresSalida:
                    try:
                        arcpy.AddMessage( "Ingresando Valor..." + str(keyvaluein) + "....(" + str(Numerador) + " de " + str(count) + ")")
                        rowin = valoresEntrada[keyvaluein]
                        rowin=list(rowin)
                        rowin[indxdiain] = datetime.datetime(rowin[indxanioin], rowin[indxmesin], rowin[indxdiain])

                        rowin[indxdepin] = rowin[indxdepin] + "-" + rowin[indxmunin]
                        if indxnomin != None:
                            rowin.insert(indxnomin, "")
                        pointCentroid = arcpy.Point(convertDecimal(rowin[indxLogX]), convertDecimal(rowin[indxLatY]))
                        rowin[indxLogX] = convertDecimal(rowin[indxLogX])
                        rowin[indxLatY] = convertDecimal(rowin[indxLatY])
                        rowin.pop(indxmesin)
                        rowin.pop(indxanioin - 1)
                        rowin.pop(indxmunin - 2)
                        # del rowin[0]
                        rowin.insert(0, pointCentroid)
                        rowin=tuple(rowin)
                        #print rowin
                        cursor3.insertRow(rowin)
                    except  Exception as e:
                        arcpy.AddMessage(  "Error1... "+ e.message)
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
                                print "Borrando Valor..." + str(row2[indxOut]) + "....(" + str(Numerador) + " de " + str(count) + ")"
                                cursor2.deleteRow()
                                Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..." + e.message

        edit.stopOperation()
        edit.stopEditing("True")
        del cursor3
        del valoresEntrada
        del valoresSalida
for tabla in Tablas:
    EntradaPol = tabla[0]
    print EntradaPol
    SalidaPun = tabla[1]
    print SalidaPun
    GeodatabaseSalida = tabla[2]
    print GeodatabaseSalida
    #print Campos(EntradaPol)
    FieldsIn=Campos(EntradaPol)
    FieldsOut=Campos(SalidaPun)
    #normalizarCampos(FieldsIn,FieldsOut)
    print "entrada: "+ str(FieldsIn)
    print "salida: "+ str(FieldsOut)
    actualizarValores(EntradaPol,SalidaPun,FieldsIn,FieldsOut)

arcpy.AddMessage("Proceso Terminado ...")