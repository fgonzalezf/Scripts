import arcpy, os, sys
from xlutils.copy import copy
from xlrd import open_workbook

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
xlsBase=None
for xls in listaExcel:
    if X==0:
        xlsBase=open_workbook(xls)
    else:
        xlsUnion=open_workbook(xls)
    X=1


