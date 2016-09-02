import arcpy,os,sys
def arrayCampos(FeatuareClass):
    listaCampos=arcpy.ListFields(FeatuareClass)
    listaNombres=[]
    listaNombres.append(u"OID@")
    for field in listaCampos:
        if field.name.upper()==u'SHAPE'.upper():
            listaNombres.append("SHAPE@")
        elif field.name.upper()=='OBJECTID'.upper():
            listaNombres.append(u"OID@")
        elif  field.name.upper()=='SHAPE_Length'.upper() or field.name=='SHAPE_Area'.upper():
            pass
        else:
            listaNombres.append(field.name)
    return listaNombres

def appendOutTestFeat(FeatIn, FeatOut,workspace):
    OBIDS={}
    CamposIn= arrayCampos(FeatIn)
    CamposOut= arrayCampos(FeatOut)
    #igualacion de campos
    camposIguales=[]
    for camposEnt in CamposIn:
        for camposSal in CamposOut:
            if camposEnt==camposSal:
                camposIguales.append(camposEnt)


    with arcpy.da.Editor(workspace) as edit:
        cursor2 = arcpy.da.InsertCursor(FeatOut,camposIguales)
        with arcpy.da.SearchCursor(FeatIn,camposIguales) as cursor:
            for row in cursor:
                IdNuevo=cursor2.insertRow(row)
                OBIDS[int(row[0])]=int(IdNuevo)

    del cursor2
    del row
    return OBIDS
def appendOutTestAnot(FeatIn, FeatOut,workspace):
    CamposIn= arrayCampos(FeatIn)
    CamposOut= arrayCampos(FeatOut)
    #igualacion de campos
    camposIguales=[]
    for camposEnt in CamposIn:
        for camposSal in CamposOut:
            if camposEnt==camposSal:
                camposIguales.append(camposEnt)
    with arcpy.da.Editor(workspace) as edit:
        cursor2 = arcpy.da.InsertCursor(FeatOut,camposIguales)
        with arcpy.da.SearchCursor(FeatIn,camposIguales) as cursor:
            for row in cursor:
                cursor2.insertRow(row)
    del cursor2
    del row

Entrada= r"D:\Proyecto\fernando.gonzalez\PRUEBAS\134IVC.mdb\Relieve\Curva_Nivel_Anot"
salida= r"D:\Proyecto\fernando.gonzalez\PRUEBAS\Cargue\YIMI\Prueba2\249IIC.mdb\Relieve\Curva_Nivel_Anot"
work=r"D:\Proyecto\fernando.gonzalez\PRUEBAS\Cargue\YIMI\Prueba3\249IIC.mdb"
#print arrayCampos(Entrada)

print appendOutTestFeat(Entrada, salida,work)

