import arcpy, os,sys
import xlrd as xl
arcpy.env.overwriteOutput=True
def getSheetName(file_name):
    pointSheetObj = []
    TeamPointWorkbook = xl.open_workbook(file_name)
    pointSheets = TeamPointWorkbook.sheet_names()

    return pointSheets
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

xlsFile=r"C:\Users\APN\Documents\SGC\Muestras\Excel\Libro_Indice_Cargue.xls"
GeodatabaseModelo=r"C:\Users\APN\Documents\SGC\Muestras\Muestras.gdb\Muestras"

print(getSheetName(xlsFile))

ListaHojas = getSheetName(xlsFile)

for hoja in ListaHojas:
    arcpy.ExcelToTable_conversion(xlsFile,GeodatabaseModelo+"_temp",hoja)
    tablaEntrada= GeodatabaseModelo+"_temp"
    FeatureClassSalida=GeodatabaseModelo+os.sep+hoja
    camposEntrada=Campos(tablaEntrada)
    CamposSalida=Campos(FeatureClassSalida)
    print camposEntrada
    print CamposSalida
    arcpy.Delete_management(tablaEntrada)
