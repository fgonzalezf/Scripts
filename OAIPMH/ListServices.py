# -*- coding: utf-8 -*-
import restapi, os ,sys
rest_url = 'http://srvagsp.sgc.gov.co/arcgis/rest/services'

# no authentication is required, so no username and password are supplied
ags = restapi.ArcServer(rest_url)

# get folder and service properties
print('Number of folders: {}'.format(len(ags.folders)))
print('Number of services: {}'.format(len(ags.services)))

# walk thru directories
X=0
for folders, services in ags.walk():
    #print root
    if folders!="Cartografia_Basica_IGAC" and folders!="Mapa_Metalogenico_Colombia_2002" and folders!="Utilities" and folders!="System":
        print folders

        for service in services:
            X = X + 1
            gauges = ags.getService(service)
            print(str(X)+ " : " + gauges.url)
            #print u' '.join((gauges)).encode('utf-8').strip()
        print '\n'