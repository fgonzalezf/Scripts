import urllib2,os


DatosUrsl=['https://www2.sgc.gov.co/volcanes/css/images/Volcanes/cambios-comportamiento-icono-128.svg',
           'https://www2.sgc.gov.co/volcanes/css/images/Volcanes/erupcion-inminente-icono-128.svg',
           'https://www2.sgc.gov.co/volcanes/css/images/Volcanes/erupcion-probable-icono-128.svg',
           'https://www2.sgc.gov.co/volcanes/css/images/Volcanes/volcan-activo-icono-128.svg',
           'https://www2.sgc.gov.co/volcanes/css/images/SGC_Loading.gif',
           'https://www2.sgc.gov.co/volcanes/css/images/logo.png',
           'https://www2.sgc.gov.co/volcanes/css/appvol.css',
           'https://www2.sgc.gov.co/volcanes/css/bootstrap.min.css',
           'https://www2.sgc.gov.co/volcanes/css/stylevol.css',
           'https://www2.sgc.gov.co/volcanes/js/app_v3_Vol.js',
           'https://www2.sgc.gov.co/volcanes/index.html']

for dato in DatosUrsl:
    filedata = urllib2.urlopen(dato)
    datatowrite = filedata.read()
    carpeta= r'C:\Users\Desarrollo\Downloads\volcanes'
    with open(carpeta+os.sep+dato.replace('https://www2.sgc.gov.co/volcanes/',''), 'wb') as f:
        f.write(datatowrite)