import arcpy, os, sys
from xlutils.copy import copy
from xlrd import open_workbook
from win32com.client import Dispatch

geodatabase=r"C:\Users\APN\Documents\SGC\Muestras\Muestras.gdb\Muestras"
Carpetasalida=r"C:\Users\APN\Documents\SGC\Muestras\Excel"

arcpy.env.workspace=geodatabase

ListaFeatuaresClass= arcpy.ListFeatureClasses("*")

for fc in ListaFeatuaresClass:
    print fc
    arcpy.TableToExcel_conversion(fc,Carpetasalida+os.sep+fc+".xls")

arcpy.env.workspace=Carpetasalida

listaExcel= arcpy.ListFiles()
X=0
xlsBase=""
xl = Dispatch("Excel.Application")
xl.Visible = True
for xls in listaExcel:
    if X==0:
        xlsBase=Carpetasalida+os.sep+xls
    else:
        xlsUnion=Carpetasalida+os.sep+xls

        wb1 = xl.Workbooks.Open(Filename=xlsUnion)
        wb2 = xl.Workbooks.Open(Filename=xlsBase)
        ws1 = wb1.Worksheets(1)
        ws1.Copy(Before=wb2.Worksheets(1))
        wb2.Close(SaveChanges=True)
    X=1
xl.Quit()


