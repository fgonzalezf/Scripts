#-*- coding: latin-1 -*-
import arcpy,os,sys

from openpyxl import Workbook

arcpy.env.overwriteOutput=True
DatasetEntrada= r"E:\Scripts\GDB_ZONAS\Eventos_15_1_2020.gdb\DAICMA"
excelRuta=r"C:\temp\excel2.xlsx"

Municipios=r"E:\Scripts\GDB_ZONAS\Eventos_15_1_2020.gdb\DAICMA\Municipios"
Eventos= DatasetEntrada+os.sep+"Eventos"
EventosTemp=DatasetEntrada+os.sep+"EventosTemp"
arcpy.env.overwriteOutput = True
arcpy.CreateFeatureclass_management(DatasetEntrada,"AccidentesTemp","POINT")
arcpy.AddField_management(EventosTemp,"ID","TEXT","","","250")
arcpy.AddField_management(EventosTemp,"DEPARTAMENTO___MUNICIPIO","TEXT","","","250")
X=0

ListaFilas=[["Label 1 Municipio","Municipio 2","Identificador IMsma","Label 2 Municipio","Municipio 2"]]
cursorins = arcpy.da.InsertCursor(EventosTemp, ["SHAPE@XY","ID","DEPARTAMENTO___MUNICIPIO"])

with arcpy.da.SearchCursor(Municipios, ["COD_DANE"]) as cursor:

    for row in cursor:
        #print "NOMBRE_ENT ='"+row[0].encode('latin-1').decode('latin-1')+"'"
        layerMunicipio=arcpy.MakeFeatureLayer_management(Municipios,"layerMunicipio","COD_DANE ="+str(row[0]))
        Eventos_Layer=arcpy.MakeFeatureLayer_management(Eventos,"Eventos_Layer")
        arcpy.SelectLayerByLocation_management("Eventos_Layer","INTERSECT","layerMunicipio")
        with arcpy.da.SearchCursor("Eventos_Layer", ["SHAPE@XY","cod_dane_muni","id_imsma_evento"]) as cursor2:
            for row2 in cursor2:
                if str(int(row2[1])) not in str(int(row[0])):
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

with arcpy.da.SearchCursor(Municipios, ["NOMBRE_ENT"]) as cursor3:
    for row in cursor3:
        layerMunicipio = arcpy.MakeFeatureLayer_management(Municipios, "layerMunicipio",
                                                           "NOMBRE_ENT ='" + row[0].encode('latin-1').decode(
                                                               'latin-1') + "'")
        Eventos_Layer = arcpy.MakeFeatureLayer_management(EventosTemp, "Eventos_Layer")
        arcpy.SelectLayerByLocation_management("Eventos_Layer", "INTERSECT", "layerMunicipio","500 METERS")
        with arcpy.da.UpdateCursor("Eventos_Layer", ["SHAPE@XY", "municipio", "id_imsma_evento"]) as cursor4:
            for row2 in cursor4:
                if row2[1].strip() in row[0]:
                    X = X + 1
                    arcpy.AddMessage(str(X) + "..Eventos_Borrados")
                    cursor4.deleteRow()

        arcpy.Delete_management("layerMunicipio")
        arcpy.Delete_management("Eventos_Layer")



X=0

with arcpy.da.SearchCursor(EventosTemp, ["municipio","id_imsma_evento","MunicipioGeografico"]) as cursor6:
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