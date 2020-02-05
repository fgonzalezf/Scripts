from arcgis.gis import server
server1 = server.Server("http://srvags.sgc.gov.co/arcgis/admin",gis=None,username=r"ingeominas\fgonzalezf",password="Maidenfgf45")

folders= server1.services.folders

for folder in folders:
    servicesFolder=server1.services.list(folder)
    for serviceF in servicesFolder:
        extensiones=serviceF.properties.extensions
        for ext in extensiones:
            print (ext.properties.name)
print(folders)