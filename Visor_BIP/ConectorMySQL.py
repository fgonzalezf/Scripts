import mysql.connector

cnx = mysql.connector.connect(user='gaudi_arcgis',
                                database='sgv',password='Arcgis_2017',
                                 host='172.25.3.88')

cursor = cnx.cursor()
query = ("SELECT * FROM " + tabla )
cursor.execute(query)
for (CONTRATO) in cursor:
  print("{} was hired on ".format(CONTRATO))
cnx.close()
