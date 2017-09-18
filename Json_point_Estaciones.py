#!/usr/bin/python
# -*- coding: utf-8 -*-
import arcpy, os, sys,urllib2,json,requests
target_url=""
ruta=r"C:\Temp"
arcpy.env.overwriteOutput=True
arcpy.CreatePersonalGDB_management(ruta,"borrar")



#http://cors-proxy.htmldriven.com/?url=http://www.htmldriven.com/sample.json

target_urls=["http://bdrsnc.sgc.gov.co/sismologia1/service_web/estaciones_hibridas.php",
"http://bdrsnc.sgc.gov.co/sismologia1/service_web/estaciones_rnac.php",
"http://bdrsnc.sgc.gov.co/sismologia1/service_web/estaciones_rsnc.php",
"http://bdrsnc.sgc.gov.co/sismologia1/service_web/capa_estaciones.php"]

for target_url in target_urls:
    arcpy.CreateTable_management(os.path.join(ruta,"borrar.mdb"),os.path.basename(target_url).split(".")[0])
    tabla=os.path.join(ruta,"borrar.mdb",os.path.basename(target_url).split(".")[0])
    vjson = requests.get(target_url).json()
    print(vjson[0])
    X=0
    for item in vjson:
         if X==0:
             for key in item.keys():
                 if key=="LATITUD" or key=="ALTITUD" or key=="LONGITUD":
                     arcpy.AddField_management(tabla,key,"DOUBLE")
                 elif key=="FECHA_INSTALACION" or key=="FECHA_RETIRO":
                     arcpy.AddField_management(tabla,key,"DATE")
                 else:
                     arcpy.AddField_management(tabla,key,"TEXT","","","255")
             X=1
         rows = arcpy.InsertCursor(tabla)
         row = rows.newRow()
         for key, value in item.items():
             if key=="LATITUD" or key=="ALTITUD" or key=="LONGITUD":
                row.setValue(key, float(value))
             else:
                row.setValue(key, value)
             print(str(key) +":"+str(value))
         rows.insertRow(row)
         del row
         del rows
#print json