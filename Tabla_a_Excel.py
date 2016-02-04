__author__ = 'fernando.gonzalez'

import xlwt, arcpy,os, sys


tabla=r"X:\PRUEBAS\Excel\Prueba.mdb\Invias"
excel=r'X:\PRUEBAS\Excel\example5.xls'


style = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['orange']
style.pattern = pattern

styleHeader = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']
styleHeader.pattern = pattern

#style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

rows = arcpy.SearchCursor(tabla, "", "", "Nombre; NombrePunto; Altura; Altura_D")

#Encabezado
ws.write(0, 0, "Nombre", styleHeader)
ws.write(0, 1, "NombrePunto", styleHeader)
ws.write(0, 2, "Altura", styleHeader)
ws.write(0, 3, "Altura_D", styleHeader)
X=1
for row in rows:
    if row.Nombre==row.NombrePunto:
        ws.write(X, 0, row.Nombre)
        ws.write(X, 1, row.NombrePunto)
    else:
        ws.write(X, 0, row.Nombre,style)
        ws.write(X, 1, row.NombrePunto,style)
    if row.Altura==str(int(row.Altura_D)):
        ws.write(X, 2, row.Altura)
        ws.write(X, 3, str(row.Altura_D))
    else:
        ws.write(X, 2, row.Altura,style)
        ws.write(X, 3, str(row.Altura_D),style)
    X=X+1
wb.save(excel)

