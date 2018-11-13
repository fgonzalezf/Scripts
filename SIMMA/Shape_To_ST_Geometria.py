import arcpy, os,sys,cx_Oracle

ShapeFile =r"C:\Users\Desarrollo\Downloads\PlanchasSIMMA\410\SHP_SIMMA\InvMM410_Magna.shp"
TXT= ShapeFile.replace("shp","txt")

fields = ["SHAPE@","CodSimma"]

conn = cx_Oracle.connect(user='SIMMA', password='SIMMA', dsn='SIGPROD_ODA')
cur = conn.cursor()
#
print("Correcto")
f = open (TXT,'w')



with arcpy.da.SearchCursor(ShapeFile, fields) as cursor:
        for row in cursor:

            sql = """INSERT INTO SIMMA.F35IPO_INV_POLIGONO (objectid, INV_MOVIMIENTO_MASA_ID, SHAPE) VALUES (sde.gdb_util.next_rowid('SIMMA', 'F35IPO_INV_POLIGONO'), :invet, sde.st_polygon (:shapefinal ,4686))"""
            print(sql)

            SHP= str(row[0].WKT).replace("MULTIPOLYGON","POLYGON").replace("(((","((").replace(")))","))")
            print(SHP)
            INV= row[1]
            #SHP= str(row[0].WKT).replace("MULTIPOLYGON","POLYGON").replace("(((","((").replace(")))","))")
            #insertar = """INSERT INTO SIMMA.F35IPO_INV_POLIGONO (objectid, INV_MOVIMIENTO_MASA_ID, SHAPE) VALUES   (sde.gdb_util.next_rowid('SIMMA', 'F35IPO_INV_POLIGONO'),"""+row[1]+ ","+"sde.st_polygon ('"+str(row[0].WKT).replace("MULTIPOLYGON","POLYGON").replace("(((","((").replace(")))","))")+"', 4686))"

            #print(insertar)
            if INV != 0:
                try:
                       cur.setinputsizes(invet=cx_Oracle.NUMBER, shapefinal=cx_Oracle.CLOB)
                       cur.execute(sql,invet=INV, shapefinal=SHP)
                       conn.commit()
                       f.write("insertado Correctamente... "+ str(INV) + "\n")
                except cx_Oracle.DatabaseError as ex:
                       #f.write(str(INV)+"\n")
                       error, = ex.args
                       print ('Error.code =', error.code)
                       print ('Error.message =', error.message)
                       print ('Error.offset =', error.offset)

cur.close()
f.close()

