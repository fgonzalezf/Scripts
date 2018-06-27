import cx_Oracle

conn = cx_Oracle.connect(user='SIMMA', password='simma', dsn='SIGPRU_ODA')
cur = conn.cursor()
#cur.execute('select * from '+table+' WHERE '+ Query )
print("Correcto")