#!/usr/bin/python
#-*- coding: utf-8 -*-
import restapi
import dominate
from dominate.tags import *
from restapi import admin
import arcpy

services_directory = 'http://ergit.presidencia.gov.co/arcgis/rest/services/'
ags = restapi.ArcServer(services_directory)

#tabla= r"E:\Users\fgonzalezf\Documents\Listado_Servicios\Listado.mdb\Listado"


#rows = arcpy.SearchCursor(tabla)



# connect to ArcGIS Server instance

X=0
doc = dominate.document(title='Listado servicios')
with doc:
    X=X+1
    print X
    with div():
        attr(cls='body')
        for row in ags.services:
                br()
                b(row.getValue("Nombre"))
                br()
                with p(row.getValue("Url")):
                    attr(style = "font-size:13px")




with open(r'E:\Users\fgonzalezf\Documents\Listado_Servicios\Listado2.html', 'w') as f:
    f.write(doc.render().encode('latin-1'))

