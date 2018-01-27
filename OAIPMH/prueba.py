import sys
reload(sys)
sys.setdefaultencoding("latin1")
from restapi import admin

url = 'http://srvags.sgc.gov.co/arcgis/rest/services' #server url
usr = r'ingeominas\fgonzalezf'
pw = r'Maidenfgf28'

arcserver = admin.ArcServerAdmin(url, usr, pw)

for service in arcserver.iter_services():
    print service.serviceName+"\n"
    print service.manifest()
    print "\n"