from os import getenv
import pymssql
import _mssql
import arcpy

#geodatabaseImsma=r"C:\Users\APN\Documents\APN\IMSMA.gdb"

#arcpy.env.workspace=geodatabaseImsma


conn = _mssql.connect(
    server=r'FGF',
    user=r'administrador',
    password='Maidenfgf1',
    database='SDE'
)

sqlcmd = """
DECLARE @myval int
EXEC sde.next_rowid 'DBO', 'Locations_point', @myval OUTPUT
SELECT @myval
"""
res = conn.execute_scalar(sqlcmd)
print str(res)
#cursor = conn.cursor()

#cursor.execute("""DECLARE @myval int EXEC sde.next_rowid SDE, Hazards_point, @myval OUTPUT SELECT @myval Next RowID""")
#cursor.callproc('FindPerson', ('Jane Doe',))
#cursor.callproc('sde.next_rowid', ('SDE' , 'Hazards_point'))
#for row in cursor:
    #print('row = %r' % (row,))
#conn.commit()
conn.close()