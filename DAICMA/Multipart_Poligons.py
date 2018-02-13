import arcpy, os , sys
from openpyxl import Workbook

arcpy.env.workspace = sys.argv[1]
excelRuta=sys.argv[2]
fcList = arcpy.ListFeatureClasses()
book = Workbook()

for fc in fcList:
    ListaFilas = [["Label 1", "FeatuareID", "Label 2", "Identificador IMSMA"]]
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
                    arcpy.AddMessage("FeatureID: "+";"+row[1]+";"+"hazard_localid: "+ row[2])
                    temp = ["FeatureID: ", row[1], "hazard_localid: ", row[2] ]
                    ListaFilas.append(temp)

                    partnum = 0
                    while partnum < geometry.partCount:
                        part = geometry.getPart(partnum)
                        #print arcpy.Polygon(part).pointCount
                        partnum += 1
        if len(ListaFilas)>1:
            sheet =book.create_sheet(fc)
            listaDef = tuple(ListaFilas)
            for row in listaDef:
                sheet.append(row)

book.save(excelRuta)

