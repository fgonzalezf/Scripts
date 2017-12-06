#!/usr/bin/python
# -*- coding: utf-8 -*-
import arcpy, os,sys
import xlrd as xl
arcpy.env.overwriteOutput=True

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
def normalizarDatos(row,longitud):
    row=list(row)
    for i in range(len(row)):
        if row[i]=="":
            row[i]=None
        elif(longitud[i]>0):
            if isinstance(row[i], basestring):
                row[i] = (row[i]).encode('utf-8')[0:longitud[i]]
            else:
                row[i] = str(row[i])[0:longitud[i]]

    row =tuple(row)
    return row


def getIndexField(fieldind,listFields):
    indx=-1
    indextemp=0
    for field in listFields:
        if field==fieldind:
            indx=indextemp
            break
        indextemp=indextemp+1
    return indx

def lenCampos(Feat):
    desc = arcpy.Describe(Feat)
    tipo= desc.dataType
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    if tipo=="FeatureClass":
        if desc.shapeType=="Point":
            Lista.append(0)
        else:
            Lista.append(0)
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            if fld.type=="String":
                Lista.append(fld.length)
            else:
                Lista.append(0)

    return Lista
#Variables
def Campos(Feat):
    desc = arcpy.Describe(Feat)
    tipo = desc.dataType
    Lista = []
    ListaCampos = arcpy.ListFields(Feat)
    if tipo == "FeatureClass":
        if desc.shapeType == "Point":
            Lista.append('SHAPE@XY')
        else:
            Lista.append('SHAPE@')
    for fld in ListaCampos:
        if fld.editable == True and fld.type != "Geometry":
            Lista.append(fld.name)
    return Lista

GeodatabaseModelo=r"C:\Users\APN\Documents\SGC\Muestras\mg100k_2.gdb\Muestras"
xlsFile=r"C:\Users\APN\Documents\SGC\Muestras\LibroIndiceMuestras_27_11_2017.xls"

print(getSheetName(xlsFile))

ListaHojas = getSheetName(xlsFile)


for hoja in ListaHojas:
    print hoja
    arcpy.ExcelToTable_conversion(xlsFile,os.path.dirname(GeodatabaseModelo)+os.sep+hoja+"_tabla",hoja)
arcpy.env.workspace=os.path.dirname(GeodatabaseModelo)

listaTablas = arcpy.ListTables("*_tabla")

for hoja in listaTablas:
    tablaEntrada= os.path.dirname(GeodatabaseModelo)+os.sep+hoja
    FeatureClassSalida=GeodatabaseModelo+os.sep+hoja.replace("_tabla","")
    camposEntrada=Campos(tablaEntrada)
    CamposSalida=Campos(FeatureClassSalida)
    longitudCamposSal=lenCampos(FeatureClassSalida)
    edit = arcpy.da.Editor(os.path.dirname(GeodatabaseModelo))
    #edit.startEditing(True,False)
    #edit.startOperation()
    cursorIns = arcpy.da.InsertCursor(FeatureClassSalida, CamposSalida)
    print(hoja)
    with arcpy.da.SearchCursor(tablaEntrada, camposEntrada) as cursor:
        #print cursor.fields
        for row in cursor:
            try:
                if hoja=="DatacionesRadiometricas":
                    indxX=getIndexField("CoordenadaX",cursor.fields)
                    indxY=getIndexField("CoordenadaY",cursor.fields)
                else:
                    indxX=getIndexField("Este",cursor.fields)
                    indxY=getIndexField("Norte",cursor.fields)
                rowin=row
                rowin = list(rowin)
                pointCentroid=(float(row[indxX]),float(row[indxY]))
                rowin.insert(0,pointCentroid)
                rowin = tuple(rowin)
                rowin=normalizarDatos(rowin,longitudCamposSal)
                print (rowin)
                cursorIns.insertRow(rowin)
            except Exception as ex:
                arcpy.AddMessage(ex.message)
    #print camposEntrada
    #print CamposSalida
    #edit.stopOperation()
    #edit.stopEditing(True)
    arcpy.Delete_management(tablaEntrada)

