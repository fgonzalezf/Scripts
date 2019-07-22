import arcpy, os, sys
from openpyxl import load_workbook

excel = r"C:\Users\APN\Downloads\Modelo_protestas\dominios.xlsx"
Geodatabase=r"C:\Users\APN\Downloads\Modelo_protestas\Protestas.gdb"
wb = load_workbook(filename = excel)

arcpy.env.overwriteOutput=True

for sheet in wb.get_sheet_names():
    print "Exportando..... "+ sheet
    arcpy.ExcelToTable_conversion(excel,Geodatabase+os.sep+sheet,sheet)
    arcpy.TableToDomain_management(Geodatabase+os.sep+sheet,"Coded","Description",Geodatabase,sheet)
    arcpy.Delete_management(Geodatabase+os.sep+sheet,sheet)