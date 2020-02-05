from arcgis.gis import GIS
gis = GIS("http://srvags.sgc.gov.co/arcprod/", "portaladmin","portalSGC2018")

gis_servers = gis.admin.servers.list()
server1 = gis_servers[0]
servicios = server1.services.list()
Carpetas = server1.services.folders

print (server1)
print (Carpetas)