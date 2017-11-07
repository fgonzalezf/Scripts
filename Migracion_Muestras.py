import arcpy, os,sys
import xlrd as xl
arcpy.env.overwriteOutput=True
def getSheetName(file_name):
    pointSheetObj = []
    TeamPointWorkbook = xl.open_workbook(file_name)
    pointSheets = TeamPointWorkbook.sheet_names()

    return pointSheets
def normalizarDatos(row):
    row=list(row)
    for i in range(len(row)):
        if row[i]=="":
            row[i]=None
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

def Campos(Feat):
    desc = arcpy.Describe(Feat)
    tipo= desc.dataType
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
#Variables

xlsFile=r"C:\Users\Fernando\Documents\Muestras\CARGUE\Libro_indice.xls"
GeodatabaseModelo=r"C:\Users\Fernando\Documents\Muestras\CARGUE\Origen_Bogota\Muestras.mdb\Muestras"

print(getSheetName(xlsFile))

ListaHojas = getSheetName(xlsFile)



for hoja in ListaHojas:

    arcpy.ExcelToTable_conversion(xlsFile,os.path.dirname(GeodatabaseModelo)+os.sep+"temp",hoja)
    tablaEntrada= os.path.dirname(GeodatabaseModelo)+os.sep+"temp"
    FeatureClassSalida=GeodatabaseModelo+os.sep+hoja
    camposEntrada=Campos(tablaEntrada)
    CamposSalida=Campos(FeatureClassSalida)

    edit = arcpy.da.Editor(os.path.dirname(GeodatabaseModelo))
    edit.startEditing()
    edit.startOperation()
    cursorIns = arcpy.da.InsertCursor(FeatureClassSalida, CamposSalida)
    print camposEntrada
    print CamposSalida
    with arcpy.da.SearchCursor(tablaEntrada, camposEntrada) as cursor:
        #print cursor.fields
        for row in cursor:
            indxX=getIndexField("Este",cursor.fields)
            indxY=getIndexField("Norte",cursor.fields)
            rowin=row
            rowin = list(rowin)
            pointCentroid=(row[indxX],row[indxY])
            rowin.insert(0,pointCentroid)
            rowin = tuple(rowin)
            rowin=normalizarDatos(rowin)
            cursorIns.insertRow(rowin)
    #print camposEntrada
    #print CamposSalida
    edit.stopOperation()
    edit.stopEditing()
    arcpy.Delete_management(tablaEntrada)

