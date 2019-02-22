import urllib2,os


DatosUrsl=['https://www2.sgc.gov.co/sismos/sismos/css/images/SGC_Loading.gif',
           'https://www2.sgc.gov.co/sismos/sismos/css/images/intensidad-64.svg',
           'https://www2.sgc.gov.co/sismos/sismos/css/images/localizacion-64.svg',
           'https://www2.sgc.gov.co/sismos/sismos/css/images/magnitud-64.svg',
           'https://www2.sgc.gov.co/sismos/sismos/css/images/magnitud.svg',
           'https://www2.sgc.gov.co/sismos/sismos/css/images/profundidad-64.svg',
           'https://www2.sgc.gov.co/sismos/sismos/css/images/profundidad.svg',
           'https://www2.sgc.gov.co/sismos/sismos/css/app.css',
           'https://www2.sgc.gov.co/sismos/sismos/css/bootstrap.min.css',
           'https://www2.sgc.gov.co/sismos/sismos/css/style.css',
           'https://www2.sgc.gov.co/sismos/sismos/images/loading.gif',
           'https://www2.sgc.gov.co/sismos/sismos/images/logo.png',
           'https://www2.sgc.gov.co/sismos/sismos/images/sus-24.svg',
           'https://www2.sgc.gov.co/sismos/sismos/js/EstacionesLayer.js',
           'https://www2.sgc.gov.co/sismos/sismos/js/LimiteMaritimoLayer.js',
           'https://www2.sgc.gov.co/sismos/sismos/js/ModConsulta.js',
           'https://www2.sgc.gov.co/sismos/sismos/js/app_v5.js',
           'https://www2.sgc.gov.co/sismos/sismos/ultimos-sismos.html']

for dato in DatosUrsl:
    filedata = urllib2.urlopen(dato)
    datatowrite = filedata.read()
    carpeta= r'C:\Users\fgonzalezf\Downloads\sismos'
    with open(carpeta+os.sep+dato.replace('https://www2.sgc.gov.co/sismos/sismos/',''), 'wb') as f:
        f.write(datatowrite)