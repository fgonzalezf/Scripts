import arcpy,os,sys
def arrayCamposFeat(FeatuareClass):
    listaCampos=arcpy.ListFields(FeatuareClass)
    listaNombres=[]
    for field in listaCampos:
        if field.name.upper()==u'SHAPE'.upper():
            listaNombres.append("SHAPE@")
        elif field.name.upper()=='OBJECTID'.upper():
            listaNombres.append(u"OID@")
        elif  field.name.upper()=='SHAPE_Length'.upper() or field.name.upper()=='SHAPE_Area'.upper() or field.name.upper()=='OVERRIDE'.upper():
            pass
        else:
            listaNombres.append(field.name.upper())
    return listaNombres

def arrayCamposAnot(FeatuareClass):
    listaCampos=arcpy.ListFields(FeatuareClass)
    listaNombres=[]
    for field in listaCampos:
        if field.name.upper()==u'SHAPE'.upper():
            listaNombres.append("SHAPE@")
        elif field.name.upper()=='OBJECTID'.upper():
            listaNombres.append(u"OID@")
        elif  field.name.upper()=='SHAPE_Length'.upper() or field.name.upper()=='SHAPE_Area'.upper():
            pass
        else:
            listaNombres.append(field.name.upper())
    return listaNombres

def appendOutTestFeat(FeatIn, FeatOut,workspace):
    OBIDS={}
    CamposIn= arrayCamposFeat(FeatIn)
    CamposOut= arrayCamposFeat(FeatOut)
    camposIguales=[]
    for camposEnt in CamposIn:
        for camposSal in CamposOut:
            if camposEnt==camposSal:
                camposIguales.append(camposEnt)
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(True, False)
    edit.startOperation()
    cursor2 = arcpy.da.InsertCursor(FeatOut,camposIguales)
    with arcpy.da.SearchCursor(FeatIn,camposIguales) as cursor:
        for row in cursor:
            IdNuevo=cursor2.insertRow(row)
            OBIDS[int(row[0])]=int(IdNuevo)
    edit.stopOperation()
    edit.stopEditing(True)
    del cursor2
    del row
    return OBIDS
def appendOutTestAnot(FeatIn, FeatOut,workspace):
    CamposIn= arrayCamposAnot(FeatIn)
    CamposOut= arrayCamposAnot(FeatOut)
    print CamposIn
    print CamposOut
    #igualacion de campos
    camposIguales=[]

    for camposEnt in CamposIn:
        for camposSal in CamposOut:
            if camposEnt==camposSal:
                camposIguales.append(camposEnt)
    print camposIguales
    #with arcpy.da.Editor(workspace) as edit:
        #print edit.isEditing
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(True, False)
    edit.startOperation()
    cursor2 = arcpy.da.InsertCursor(FeatOut,camposIguales)
    with arcpy.da.SearchCursor(FeatIn,camposIguales) as cursor:
            for row in cursor:
                cursor2.insertRow(row)
    edit.stopOperation()
    edit.stopEditing(True)

    del cursor2
    del row

Entrada= r"D:\Proyecto\fernando.gonzalez\PRUEBAS\Cargue\YIMI\Prueba3\249IIC.mdb\Relieve\Curva_Nivel_Anot"
salida= r"D:\Proyecto\fernando.gonzalez\PRUEBAS\Cargue\YIMI\Prueba3\25K_29_04_2016_GEODATABASE_ANOTACIONES.mdb\Relieve\Curva_Nivel_Anot"
work=r"D:\Proyecto\fernando.gonzalez\PRUEBAS\Cargue\YIMI\Prueba3\25K_29_04_2016_GEODATABASE_ANOTACIONES.mdb"
#print arrayCampos(Entrada)

print appendOutTestAnot(Entrada,salida,work)

