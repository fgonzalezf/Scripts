import arcpy,os,sys

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

Tablas=[]

Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\epis.odc\.view_informes",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_informes',r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\epis.odc\.view_contratos",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_contratos',r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\epis.odc\.view_pozos",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_pozos',r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\epis.odc\.view_sismica2d",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_sismica2d',r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\epis.odc\.view_sismica3d",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_sismica3d',r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde'])

for tabla in Tablas:
    Entrada=r"C:\Users\Desarrollo\Documents\EPIS\epis.odc\.view_informes"
    Salida=r'C:\Users\Desarrollo\Documents\EPIS\Tablas.gdb\T_view_informes'
    GeodatabaseSalida=r'C:\Users\Desarrollo\Documents\EPIS\Tablas.gdb'
    CampoIdentificador='CONTRATO'

    arcpy.env.workspace=GeodatabaseSalida
    desc = arcpy.Describe(Salida)
    tipo= desc.dataType
    print tipo

    print Campos(Entrada)
    Fields=Campos(Entrada,tipo,desc)
    indx = Campos.index(CampoIdentificador)

    actualizarValores(Entrada,Salida,Fields,indx)
