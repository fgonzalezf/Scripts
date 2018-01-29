#-*- coding: latin-1 -*-
import arcpy,os,sys

DatasetEntrada= r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB\Bk_GDB.gdb\DAICMA"
excelRuta=r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB"

Municipios=DatasetEntrada+os.sep+"Municipios"
Eventos= DatasetEntrada+os.sep+"Eventos"
X=0
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
        arcpy.Delete_management("layerMunicipio")
        arcpy.Delete_management("Eventos_Layer")



