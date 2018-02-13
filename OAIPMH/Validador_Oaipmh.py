import arcpy, os ,sys, urllib2

Tablametadatos = r"D:\Conexiones_SDE\OAIPMH.sde\OAIPMH.records"

contador=0
with arcpy.da.SearchCursor(Tablametadatos, ["RECORD_ID"]) as cursor:
    for row in cursor:
        try:
            contador=contador+1
            response = urllib2.urlopen('http://srvagspru.sgc.gov.co/oairequest?verb=GetRecord&identifier='+str(row[0])+'&metadataPrefix=oai_dc')
            html = response.read()
            #print str(contador)+ "...."
        except:
            print(row[0])