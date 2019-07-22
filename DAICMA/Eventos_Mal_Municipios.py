#-*- coding: latin-1 -*-
import arcpy,os,sys

from openpyxl import Workbook

DatasetEntrada= r"C:\Users\APN\Documents\APN\CENAM\CENAM_BK_1.gdb\CENAM"
excelRuta=r"C:\Temp\excel3.xlsx"

Municipios=r"C:\Users\APN\Documents\APN\CENAM\CENAM_BK_1.gdb\CENAM\Municipios_T"
Eventos= DatasetEntrada+os.sep+"Operaciones"
EventosTemp=DatasetEntrada+os.sep+"EventosTemp"
arcpy.env.overwriteOutput = True
arcpy.CreateFeatureclass_management(DatasetEntrada,"EventosTemp","POINT")
arcpy.AddField_management(EventosTemp,"CODIGO_DANE","TEXT","","","250")
arcpy.AddField_management(EventosTemp,"ID","TEXT","","","250")
arcpy.AddField_management(EventosTemp,"CODIGO_DANE_GEO","TEXT","","","250")
X=0

ListaFilas=[["Label 1 Municipio","Municipio 1","Identificador IMsma","Label 2 Municipio","Municipio 2"]]
cursorins = arcpy.da.InsertCursor(EventosTemp, ["SHAPE@XY","CODIGO_DANE","ID","CODIGO_DANE_GEO"])

with arcpy.da.SearchCursor(Municipios, ["CODIGO"]) as cursor:

    for row in cursor:
        #print "NOMBRE_ENT ='"+row[0].encode('latin-1').decode('latin-1')+"'"
        layerMunicipio=arcpy.MakeFeatureLayer_management(Municipios,"layerMunicipio","CODIGO = '"+str(int(row[0])).strip()+"'")
        Eventos_Layer=arcpy.MakeFeatureLayer_management(Eventos,"Eventos_Layer")
        arcpy.SelectLayerByLocation_management("Eventos_Layer","INTERSECT","layerMunicipio")
        with arcpy.da.SearchCursor("Eventos_Layer", ["SHAPE@XY","codMunicipioAlf5","ID"]) as cursor2:
            for row2 in cursor2:
                if row2[1].strip() not in row[0].strip():
                    X=X+1
                    temprow =list(row2)
                    temprow.append(row[0])
                    row2=tuple(temprow)
                    arcpy.AddMessage(str(X)+ "...inicial")
                    #temp = ["Municipio Atributo: " , row2[0].strip(), row2[1].strip(),"Municipio Geografico: ", row[0]]
                    cursorins.insertRow(row2)

                    #ListaFilas.append(temp)
        arcpy.Delete_management("layerMunicipio")
        arcpy.Delete_management("Eventos_Layer")
X=0
del cursorins

with arcpy.da.SearchCursor(Municipios, ["CODIGO"]) as cursor3:
    for row in cursor3:
        layerMunicipio = arcpy.MakeFeatureLayer_management(Municipios, "layerMunicipio",
                                                           "CODIGO = '"+str(row[0]).strip()+"'")
        Eventos_Layer = arcpy.MakeFeatureLayer_management(EventosTemp, "Eventos_Layer")
        arcpy.SelectLayerByLocation_management("Eventos_Layer", "INTERSECT", "layerMunicipio","500 METERS")
        with arcpy.da.UpdateCursor("Eventos_Layer", ["SHAPE@XY","CODIGO_DANE","ID"]) as cursor4:
            for row2 in cursor4:
                if row2[1].strip() in row[0].strip():
                    X = X + 1
                    arcpy.AddMessage(str(X) + "..Eventos_Borrados")
                    cursor4.deleteRow()

        arcpy.Delete_management("layerMunicipio")
        arcpy.Delete_management("Eventos_Layer")



X=0

with arcpy.da.SearchCursor(EventosTemp, ["CODIGO_DANE","ID","CODIGO_DANE_GEO"]) as cursor6:
        for row2 in cursor6:
                    X=X+1
                    arcpy.AddMessage(str(X) + ";" + "Municipio Atributo: " + ";" + row2[0].strip() + ";" + row2[1].strip() + ";" + "Municipio Geografico: " + ";" + row2[2])
                    temp = ["Municipio Atributo: " , row2[0].strip(), row2[1].strip(),"Municipio Geografico: ", row2[2]]
                    ListaFilas.append(temp)
        arcpy.Delete_management("layerMunicipio")
        arcpy.Delete_management("Eventos_Layer")

book = Workbook()
sheet = book.active

listaDef = tuple(ListaFilas)

for row in listaDef:
    sheet.append(row)

book.save(excelRuta)