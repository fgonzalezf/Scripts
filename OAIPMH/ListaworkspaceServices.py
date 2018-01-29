#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import restapi
from restapi import admin

url = 'http://srvags.sgc.gov.co/arcgis/rest/services' #server url
usr = r'ingeominas\fgonzalezf'
pw = r'Maidenfgf27'

# connect to ArcGIS Server instance
arcserver = restapi.ArcServer(url)



for service in arcserver.services:
    print service+ "/iteminfo/manifest/manifest.json"

