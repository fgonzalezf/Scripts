import arcpy, os ,sys, urllib2,time



Tablametadatos = r"F:\Conexiones_SDE\OAIPMH.sde\OAIPMH.records"

contador=0
with arcpy.da.SearchCursor(Tablametadatos, ["RECORD_ID"]) as cursor:
    for row in cursor:
        try:
            contador=contador+1
            response = urllib2.urlopen('http://srvagspru.sgc.gov.co/oairequest?verb=GetRecord&identifier='+str(row[0])+'&metadataPrefix=oai_dc')
            html = response.read()
            parteDecimal = (contador/1000.0)%1
            if parteDecimal==0:
                arcpy.AddMessage(str(contador) + "....")
                #print  (contador + "...."),
                #print str(contador)+ "...."
        except:
            arcpy.AddMessage((row[0]) +" ...  " +str(contador))
            contador = contador + 1