import urllib2,os


DatosUrsl=['http://geored2.sgc.gov.co/visor/css/popup.css',
           'http://geored2.sgc.gov.co/visor/data/main.js',
           'http://geored2.sgc.gov.co/visor/data/popup.js',
           'http://geored2.sgc.gov.co/visor/data/stations.js',
           'http://geored2.sgc.gov.co/visor/images/triangle.png',
           'http://geored2.sgc.gov.co/visor/index.html',
           'http://geored2.sgc.gov.co/visor/data/data.js']

for dato in DatosUrsl:
    filedata = urllib2.urlopen(dato)
    datatowrite = filedata.read()
    carpeta= r'C:\Users\APN\Downloads\Geored\visor'
    with open(carpeta+os.sep+dato.replace('http://geored2.sgc.gov.co/visor/',''), 'wb') as f:
        f.write(datatowrite)