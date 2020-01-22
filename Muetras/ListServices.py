#-*- coding: utf-8 -*-
import json, urllib2, sys
reload(sys)
sys.setdefaultencoding('UTF8')

server = "srvags.sgc.gov.co"
port = ""
baseUrl = "http://{}:{}/arcgis/rest/services".format(server, port)

def getCatalog():
  catalog = json.load(urllib2.urlopen(baseUrl + "/" + "?f=json"))
  print 'ROOT'
  if "error" in catalog: return
  services = catalog['services']
  for service in services:
    response = json.load(urllib2.urlopen(baseUrl + '/' + service['name'] + '/' + service['type'] + "?f=json"))
    print '  %s %s (%s)' % (service['name'], service['type'], 'ERROR' if "error" in response else 'SUCCESS')
  folders = catalog['folders']
  for folderName in folders:
    catalog = json.load(urllib2.urlopen(baseUrl + "/" + folderName + "?f=json"))
    #print folderName
    if "error" in catalog: return
    services = catalog['services']
    for service in services:
      response = json.load(urllib2.urlopen(baseUrl + '/' + service['name'] + '/' + service['type'] + "?f=json"))
      print '  %s %s (%s)' % (service['name'], service['type'], 'ERROR' if "error" in response else 'SUCCESS')

getCatalog()