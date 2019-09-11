# -*- coding: utf-8 -*-
import restapi, os ,sys
rest_url = 'http://srvags.sgc.gov.co/arcgis/rest/services'

# no authentication is required, so no username and password are supplied
ags = restapi.ArcServer(rest_url)

# get folder and service properties
print('Number of folders: {}'.format(len(ags.folders)))
print('Number of services: {}'.format(len(ags.services)))

# walk thru directories
for folders, services in ags.walk():
    #print root
    if folders!="Cartografia_Basica_IGAC" and folders!="Mapa_Metalogenico_Colombia_2002" and folders!="Utilities":
        print folders
        for service in services:
            gauges = ags.getService(service)
            print(gauges.url)
            print u' '.join((gauges.json)).encode('utf-8').strip()
        print '\n'