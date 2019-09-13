from restapi import admin

# test with your own servers
url = 'https://srvags.sgc.gov.co/arcgis/rest/services' #server url
usr = r'ingeominas\fgonzalezf'
pw = 'Maidenfgf42'

# connect to ArcGIS Server instance
arcserver = admin.ArcServerAdmin(url, usr, pw)