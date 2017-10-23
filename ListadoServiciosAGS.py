#!/usr/bin/python
#-*- coding: utf-8 -*-
import restapi
import dominate
from dominate.tags import *
from restapi import admin
import arcpy

services_directory = 'http://srvags.sgc.gov.co/arcgis/rest/services'
ags = restapi.ArcServer(services_directory)

tabla= r"C:\Users\fgonzalezf\Documents\Listado_Servicios\Listado.mdb\Listado"


rows = arcpy.SearchCursor(tabla)



# connect to ArcGIS Server instance


doc = dominate.document(title='Listado servicios')
with doc:
    with div():
        attr(cls='body')
        for row in rows:
                br()
                b(row.getValue("Nombre"))
                br()
                with p(row.getValue("Url")):
                    attr(style = "font-size:13px")




with open(r'C:\Users\fgonzalezf\Documents\Listado_Servicios\Listado.html', 'w') as f:
    f.write(doc.render().encode('latin-1'))

