import arcpy,os, sys
from openpyxl import Workbook

arcpy.env.workspace = r"C:\Users\Desarrollo\Documents\APN\Bk_GDB.gdb\DAICMA"
excelRuta=r"C:\Users\Desarrollo\Documents\APN"
fcList = arcpy.ListFeatureClasses()

ListaFilas=[["Label 1","FeatuareID","Label 2","Identificador IMSMA"]]
for fc in fcList:
    print fc
    if fc!="Colombia" and fc!="Sectores" and fc!="Eventos" and fc!="Municipios" and fc!="Departamento" and fc!="Zonas"and fc!="Estudios_No_Tecnicos_Punto" and fc!="Estudios_Tecnicos_Punto":
        fields=[]
        if fc=="Estudios_Tecnicos" or fc=="Areas_Despejadas" :
            fields=["SHAPE@","FeatureID","hazreduc_localid"]
        elif fc=="Estudios_No_Tecnicos":
            fields=["SHAPE@","FeatureID","hazreduc_localid"]
        else:
            fields=["SHAPE@","FeatureID","hazard_localid"]
        with arcpy.da.SearchCursor(fc, fields) as cursor:
            for row in cursor:
                geometry = row[0]
                if geometry.isMultipart == True:
                    print "FeatureID: "+";"+row[1]+";"+"hazard_localid: "+ row[2]
                    temp = ["FeatureID: ", row[1], "hazard_localid: ", row[2] ]
                    ListaFilas.append(temp)

                    partnum = 0
                    while partnum < geometry.partCount:
                        part = geometry.getPart(partnum)
                        #print arcpy.Polygon(part).pointCount
                        partnum += 1

book = Workbook()
sheet = book.active

listaDef = tuple(ListaFilas)
for row in listaDef:
    sheet.append(row)

book.save(excelRuta+os.sep+'corbatines.xlsx')

