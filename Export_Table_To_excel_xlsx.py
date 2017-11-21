import arcpy, os, sys
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation


def campos(Feat):
    listadoCampos=[]
    fields=arcpy.ListFields(Feat)
    for field in fields:
        if field.editable==True and field.type!="Geometry":
            Temparr=[]
            Temparr.append(field.name)
            Temparr.append(field.type)
            Temparr.append(field.length)
            listadoCampos.append(Temparr)
    return listadoCampos


def exportXLSX(Feat,ListFields,wb):
    ws = wb.create_sheet(title=os.path.basename(Feat))
    print
    for col in range(1, len(ListFields)):
            dv=None
            if ListFields[col][1]=="String":
                dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1=ListFields[col][2])
            elif ListFields[col][1]=="Double":
                dv = DataValidation(type="decimal")
            elif ListFields[col][1]=="SmallInteger" or ListFields[col][1]=="Integer":
                dv = DataValidation(type="whole")
            elif ListFields[col][1]=="Date":
                dv = DataValidation(type="date")
            ws.cell(column=col, row=1, value="{0}".format(ListFields[col][0]))
            dv.ranges.append()
            for row in range(2, 65536):
                dv.add(ws.cell(column=col, row=row))







FeatEntrada =r"C:\Users\Desarrollo\Documents\Muestras\Origen_Bogota\mg100k.gdb\Muestras\Gravas"

wb = Workbook()
dest_filename = r'C:\Users\Desarrollo\Documents\Muestras\Nuevo2.xlsx'
ListaCampos=campos(FeatEntrada)
exportXLSX(FeatEntrada,ListaCampos,wb)

wb.save(filename = dest_filename)