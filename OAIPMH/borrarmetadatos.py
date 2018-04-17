import arcpy, os ,sys, urllib2,time



Tablametadatos = sys.argv[1]

contador=0
with arcpy.da.UpdateCursor(Tablametadatos, ["RECORD_ID"]) as cursor:
    for row in cursor:
        if str(row[0])=="WELL_MORC0008NN":
            try:
                cursor.deleteRow()
                arcpy.AddMessage(str(row[0]))
            except:
                arcpy.AddMessage((row[0]) +" ...  " )