import arcpy,os,sys,xlsxwriter

Excel_Salida = sys.argv[1]

workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

for row in range(0, 5):
    worksheet.write(row, 0, 'Hello')