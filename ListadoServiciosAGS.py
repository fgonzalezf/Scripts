#!/usr/bin/python
#-*- coding: utf-8 -*-
import restapi
import dominate
from dominate.tags import *

services_directory = 'http://srvags.sgc.gov.co/arcgis/rest/services'
ags = restapi.ArcServer(services_directory)

doc = dominate.document(title='Listado servicios')
with doc:
    with div():
        attr(cls='body')
        for service in ags.services:
            with div():
                p(service)

with open(r'C:\Users\APN\Documents\VICTIMAS\Listado.html', 'w') as f:
    f.write(doc.render().encode('latin-1'))

