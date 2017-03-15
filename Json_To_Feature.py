__author__ = 'fgonzalezf'
import json
import urllib2

url="http://bdrsnc.sgc.gov.co/sismologia1/service_web/capa_estaciones.php"
response = urllib2.urlopen(url)
for line in response:
    if "[{" in line:
        data = json.loads(line)
        for dat in data:
            print dat
            for keys,values in dat.items():
                print keys




