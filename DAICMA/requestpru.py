import arcpy, os, sys, urllib2

tabla=r"C:\Users\APN\Documents\SGC\OAIPMH\h.mdb\records"
X=0
with arcpy.da.UpdateCursor(tabla, "RECORD_ID") as cursor:
    for row in cursor:
        X=X+1
        print str(X)+ "..."
        try:
            response = urllib2.urlopen('http://srvagspru.sgc.gov.co/oairequest?verb=GetRecord&identifier='+str(row[0])+'&metadataPrefix=oai_dc')
            headers = response.read()
        except:
            print "error en Id..."+str(row[0])
            print str(X)