import restapi, os ,sys
services_directory = 'http://ergit.presidencia.gov.co/arcgis/rest/services/'
ags = restapi.ArcServer(services_directory)
print ags.services