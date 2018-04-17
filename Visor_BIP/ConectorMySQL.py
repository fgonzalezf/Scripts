import mysql.connector






#query = ("SELECT * FROM " + tabla )


def CountMysql(tabla):
    cnx = mysql.connector.connect(user='gaudi_arcgis', database='sgv',password='Arcgis_2017',host='172.25.3.88')
    cursor = cnx.cursor()
    query ="select count(*) from "+ tabla
    #query = ("DESCRIBE " + tabla )
    cursor.execute(query)
    count=0
    for row in cursor:
       count=row[0]
    return count

print CountMysql("view_contratos")
