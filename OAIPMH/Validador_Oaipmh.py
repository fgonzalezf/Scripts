import arcpy, os ,sys, urllib2

Tablametadatos = r"D:\Conexiones_SDE\OAIPMH.sde\OAIPMH.records"


with arcpy.da.SearchCursor(Tablametadatos, ["RECORD_ID"]) as cursor:
    for row in cursor:
        try:
            response = urllib2.urlopen('http://srvagspru.sgc.gov.co/oairequest?verb=GetRecord&identifier='+str(row[0])+'&metadataPrefix=oai_dc')
            html = response.read()
        except:
            print(row[0])