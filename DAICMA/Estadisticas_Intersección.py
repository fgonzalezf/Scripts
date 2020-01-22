import arcpy, os, sys



TablaEntrada=r"in_memory\TablaInterseccion"
CapaZonas=r"C:\Users\fgonzalezf\Downloads\prueba_Interseccion\Eeventos_20_01_2020.gdb\DAICMA\Municipios"
CapaPuntos =r"C:\Users\fgonzalezf\Downloads\prueba_Interseccion\Eeventos_20_01_2020.gdb\DAICMA\Eventos"
CampoSalida="No_eventos"
Geodatabase=r"C:\Users\fgonzalezf\Downloads\prueba_Interseccion\Eeventos_20_01_2020.gdb"
#verificar si campo de Salida existe en capa de entrada
arcpy.env.overwriteOutput=True
def CampoExiste(Feat,Campo):
    ListaCampos=arcpy.ListFields(Feat)
    existe=False
    for fld in ListaCampos:
        if fld.name == Campo:
            existe=True
    if not existe:
        arcpy.AddField_management(Feat,Campo,"SHORT","","","",Campo)
    return existe
def ValoresEntrada(Feat,fields):
    datos = {}
    tindx=0
    indx = 0
    CampoIdentificador="OBJECTID_1"
    for field in fields:
        if field==CampoIdentificador:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[indx]] =row
    return datos
#Creacion de Campo

def CalculoCampo (Feat,Campo,Tabla):
    objId="OBJECTID"
    objIdUn="OBJECTID_1"
    fields=[]
    fields.append(objId)
    fields.append(Campo)
    indx = fields.index(objId)
    valoresEntrada = ValoresEntrada(Tabla, ["OBJECTID_1","PNT_COUNT"])
    result = arcpy.GetCount_management(Tabla)
    count = int(result.getOutput(0))
    Numerador = 0
    edit = arcpy.da.Editor(Geodatabase)
    edit.startEditing()
    edit.startOperation()
    Controlvalores = []
    with arcpy.da.UpdateCursor(Feat, fields) as cursor:
        for row in cursor:
            keyvalue = row[indx]
            if keyvalue in valoresEntrada:
                if keyvalue not in Controlvalores:
                    try:
                        Numerador = Numerador + 1
                        print "Actualizando Valor..." + str(row[indx]) + "....(" + str(Numerador) + " de " + str(
                            count) + ")"
                        cursor.updateRow(valoresEntrada[keyvalue])
                        Controlvalores.append(keyvalue)
                    except Exception as e:
                        print "Error..." + e.message
    edit.stopOperation()
    edit.stopEditing("True")

CampoExiste(CapaZonas,CampoSalida)
arcpy.TabulateIntersection_analysis(CapaZonas,"OBJECTID",CapaPuntos,TablaEntrada)
CalculoCampo(CapaZonas,CampoSalida,TablaEntrada)
del TablaEntrada







