import arcpy, os,sys
import xlrd as xl

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

ExcelEntrada =r"C:\Users\APN\Documents\SGC\Muestras\LibroIndiceMuestras_27_11_2017.xls"
GeodatabaseSalida=r"C:\Users\APN\Documents\SGC\Muestras\Prueba1.gdb"

ListaHojas = getSheetName(ExcelEntrada)

for hoja in ListaHojas:
    print hoja
    arcpy.ExcelToTable_conversion(ExcelEntrada,GeodatabaseSalida+os.sep+hoja+"tabla",hoja)