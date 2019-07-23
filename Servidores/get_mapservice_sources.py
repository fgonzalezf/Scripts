'''
Script to list data sources (feature classes paths) that are served by a map service
as well as map document that was used for publishing a service.

The script will report this information for all map services on the ArcGIS Server.
It is required to have an Administrator level user account to be able to log in into
the ArcGIS Server Administrator Directory.
'''

import collections
import requests
import xmltodict
from arcrest.manageags import AGSAdministration
from arcrest import AGSTokenSecurityHandler

#----------------------------------------------------------------------
def get_service_manifest(token,service_url):
    '''
    Return service manifest, based on this url
    http://localhost:6080/arcgis/admin/services/servicename.MapServer/iteminfo/manifest/manifest.xml
    a shorter version of manifest can be obtained from a JSON manifest, available via REST API:
    http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#//02r3000001vt000000
    '''
    metadata_url = '{0}/iteminfo/manifest/manifest.xml'.format(service_url)
    xml_data = requests.get(metadata_url,params={'token':token}).content
    return xml_data

#----------------------------------------------------------------------
def get_connection(data):
    '''return database connection string for the service'''
    return data['SVCManifest']['Databases']['SVCDatabase']['OnPremiseConnectionString']

#----------------------------------------------------------------------
def get_datasets(data):
    '''return a list of paths to datasets such as feature classes used by service'''


    if data['SVCManifest']['Databases']['SVCDatabase']['ByReference'] == 'false':
            return 'Service data has been copied'

    service_items = []
    try:
        datasets = data['SVCManifest']['Databases']['SVCDatabase']['Datasets']['SVCDataset']
    except:
        datasets = data['SVCManifest']['Databases']['SVCDatabase']['Datasets']
    if isinstance(datasets,list):
            for ds in datasets:
                service_items.append(ds['OnPremisePath'])
    elif isinstance(datasets, collections.OrderedDict):
            service_items.append(datasets['OnPremisePath'])

    return service_items

#----------------------------------------------------------------------
def get_resource(data):
    '''return a map document path that was used during the publishing'''
    resources = data['SVCManifest']['Resources']['SVCResource']

    #getting path of mxd document published
    if isinstance(resources,list):
        for res in resources:
            return res['OnPremisePath']
    elif isinstance(resources, collections.OrderedDict):
        return resources['OnPremisePath']

#----------------------------------------------------------------------
def get_services(server,port,user,pwd):
    '''return a list of dictionaries with service name, folder, type and URL;
     the list is sorted by service name'''
    ags_admin_url = r'http://{0}:{1}/arcgis/admin'.format(server,port)
    ags_security_handler = AGSTokenSecurityHandler(username=user,password=pwd,org_url=ags_admin_url)

    ags_obj = AGSAdministration(ags_admin_url,ags_security_handler)
    services = ags_obj.services.find_services(service_type='MAPSERVER')
    services = [s for s in services if s['serviceName'] != 'SampleWorldCities']
    return sorted(services,key=lambda s: s['serviceName'])

#----------------------------------------------------------------------
def get_token(server,port,user,pwd):
    '''return a token as string from AGS'''
    ags_admin_url = r'http://{0}:{1}/arcgis/admin'.format(server,port)
    ags_security_handler = AGSTokenSecurityHandler(username=user,password=pwd,org_url=ags_admin_url)
    return ags_security_handler.token

#----------------------------------------------------------------------
def main():
    '''report information about services'''

    server = 'srvags.sgc.gov.co'
    port = 80
    user = r'ingeominas\fgonzalezf'
    pwd = 'Maidenfgf41'

    token = get_token(server, port, user, pwd)
    services = get_services(server, port, user, pwd)

    #iterating service and reporting information about its datasets and resources
    for service in services:
        folder_name = service['folderName'] if service['folderName'] != '/' else ''
        if "Atlas_2016_Geofisica"not in service['serviceName'] and "Mapa_Base"not in service['serviceName']:
         print '{0}/{1}'.format(folder_name,service['serviceName']).center(50,'-')
         xml_string = get_service_manifest(token,service['URL'])

         #convert string xml into a Python ordered dict
         data = dict(xmltodict.parse(xml_input=xml_string,encoding='UTF-8'))

         #get datasets and resources
         #db_connection = get_connection(data)
         datasets = get_datasets(data)
         resource = get_resource(data)
         print 'Datasets:','\n', datasets
         print 'Map document:','\n', resource
         print

if __name__ == '__main__':
    main()