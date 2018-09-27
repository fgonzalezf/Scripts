import arcpy ,os,sys
arcpy.env.overwriteOutput=True
Actualizar=True
Borrar=True

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

def actualizarValores(Featin, FeatOut, fields,indx):
        valoresEntrada = ValoresEntrada(Featin,fields)
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
                                conjRow=set(valoresEntrada[keyvalue])
                                conjRow2=set(row2)
                                final = conjRow - conjRow2
                                #print final
                                if len(final) > 0:
                                    print "Actualizando Valor..."+ str(row2[indx])+ "....("+str(Numerador)+ " de "+str(count)+")"
                                    cursor2.updateRow(valoresEntrada[keyvalue])
                                    Controlvalores.append(keyvalue)
                            except Exception as e:
                                print "Error..."+ e.message

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
                try:
                    print "Ingresando Valor..." + str(keyvaluein) + "....(" + str(Numerador) + " de " + str(count) + ")"
                    cursor3.insertRow(valoresEntrada[keyvaluein])
                except  Exception as e:
                    print  "Error... "+ e.message
        edit.stopOperation()
        edit.stopEditing("True")

        edit.startEditing()
        edit.startOperation()
        valoresEntrada = ValoresEntrada(Featin, fields)
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

def exportarGDB(entrada,carpetaTemp):
    arcpy.env.workspace=entrada
    ListaFeat= arcpy.ListFeatureClasses()
    arcpy.CreateFileGDB_management(carpetaTemp,"IMSMA.gdb")
    arcpy.CreateFeatureDataset_management(carpetaTemp+os.sep+"IMSMA.gdb","IMSMA",r"E:\Scripts\Temp\GCS_WGS_1984.prj")
    salida = carpetaTemp+os.sep+"IMSMA.gdb"+os.sep+"IMSMA"
    for fc in ListaFeat:
        arcpy.FeatureClassToFeatureClass_conversion(fc,salida,fc)
    return salida


IMSMAGDB=r"C:\Users\Administrator\Downloads\IMSMA.gdb"
GeodatabaseSalida=r"E:\Scripts\SDE.sde\SDE.DBO.CAPAS_IMSMA"
carpeta = r"E:\Scripts\Temp"
print "Reparando Geometria"
Entrada=exportarGDB(IMSMAGDB,carpeta)
arcpy.env.workspace=Entrada
ListaFeaturesClass=arcpy.ListFeatureClasses()
Tablas=[]
for fc in ListaFeaturesClass:
    arcpy.RepairGeometry_management(fc,"True")
    Tablas.append([Entrada+os.sep+fc,GeodatabaseSalida+os.sep+fc,os.path.dirname(GeodatabaseSalida)])

print "Proceso Iniciado"

for tabla in Tablas:
    Salida=tabla[1]
    GeodatabaseSalida=tabla[2]
    Entrada = tabla[0]
    CampoIdentificador="FeatureID"
    arcpy.env.workspace=GeodatabaseSalida
    desc = arcpy.Describe(Salida)
    tipo= desc.dataType
    print tipo
    print Campos(Entrada,tipo,desc)
    Fields=Campos(Entrada,tipo,desc)
    indx = Fields.index(CampoIdentificador)
    actualizarValores(Entrada,Salida,Fields,indx)
