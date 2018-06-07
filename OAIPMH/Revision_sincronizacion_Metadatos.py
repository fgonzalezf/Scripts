import cx_Oracle, arcpy
con =  db = cx_Oracle.connect('OAIPMH', 'OAIPMH', '172.25.3.110:1548/SIGPROD')
cursor = con.cursor ()
sql="SELECT OBJECTID  FROM records ORDER BY OBJECTID DESC"
cursor.execute(sql)
OBID1 = int(cursor.fetchall ()[0][0])+2
print  con.version
print "conexion"
con.close()