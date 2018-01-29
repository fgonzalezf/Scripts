#-*- coding: latin-1 -*-
import arcpy,os,sys

from openpyxl import Workbook

DatasetEntrada= r"C:\Users\Desarrollo\Documents\APN\Bk_GDB.gdb\DAICMA"
excelRuta=r"C:\Users\Desarrollo\Documents\APN"

Municipios=DatasetEntrada+os.sep+"Municipios"
Eventos= DatasetEntrada+os.sep+"Eventos"
X=0

ListaFilas=[["Label 1 Municipio","Municipio 2","Identificador IMsma","Label 2 Municipio","Municipio 2"]]
with arcpy.da.SearchCursor(Municipios, ["NOMBRE_ENT"]) as cursor:

    for row in cursor:
        #print "NOMBRE_ENT ='"+row[0].encode('latin-1').decode('latin-1')+"'"
        layerMunicipio=arcpy.MakeFeatureLayer_management(Municipios,"layerMunicipio","NOMBRE_ENT ='"+row[0].encode('latin-1').decode('latin-1')+"'")
        Eventos_Layer=arcpy.MakeFeatureLayer_management(Eventos,"Eventos_Layer")
        arcpy.SelectLayerByLocation_management("Eventos_Layer","INTERSECT","layerMunicipio")
        with arcpy.da.SearchCursor("Eventos_Layer", ["municipio","id_imsma_evento"]) as cursor2:
            for row2 in cursor2:
                if row2[0].strip()!=row[0].strip():
                    X=X+1
                    print str(X)+";"+"Municipio Atributo: "+";"+ row2[0].strip()+";"+row2[1].strip()+";"+"Municipio Geografico: "+";"+ row[0]
                    temp = ["Municipio Atributo: " , row2[0].strip(), row2[1].strip(),"Municipio Geografico: ", row[0]]
                    ListaFilas.append(temp)
        arcpy.Delete_management("layerMunicipio")
        arcpy.Delete_management("Eventos_Layer")


book = Workbook()
sheet = book.active

listaDef = tuple(ListaFilas)
for row in listaDef:
    sheet.append(row)

book.save(excelRuta+os.sep+'iterbycols.xlsx')