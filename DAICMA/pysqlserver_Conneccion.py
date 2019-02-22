from os import getenv
import pymssql
import _mssql
import arcpy,os

geodatabaseImsma=r"C:\Users\Administrator\Downloads\IMSMA.gdb"

arcpy.env.workspace=geodatabaseImsma

listFeatuares = arcpy.ListFeatureClasses()
for fc in listFeatuares:
    print fc

def Campos(Feat,tipo,desc):
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    if tipo=="FeatureClass":
        Lista.append('SHAPE@WKT')
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name)
    return Lista

def ValoresEntrada(Feat,index):
    describeType = arcpy.Describe(Feat).dataType
    describeGeom = arcpy.Describe(Feat).shapeType
    fields=Campos(Feat,describeType,describeGeom)
    datos = {}
    tindx=0
    indx = 0
    for field in fields:
        if field==index:
            indx=tindx
        tindx=tindx+1
    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
            sqlInicio="INSERT INTO "+ os.path.basename(Feat) + "_evw " + str(tuple(fields)).replace("u'","'").replace("SHAPE@WKT","SHAPE").replace("'","") + " VALUES ( geometry::STGeomFromText( ' " + row[0]+"' , 4326 )"
            sqlfinal=""
            for x in range(1,len(fields)):
                if row[x]==None:
                    sqlfinal =   sqlfinal +","+ "NULL"
                elif isinstance(row[x],basestring):
                    sqlfinal = sqlfinal + "," + "'"+row[x]+"'"
                elif isinstance(row[x],(int, long ,float ,complex)):
                    sqlfinal =  sqlfinal + "," + str(row[x])

def ValoresSalida (tabla, index):

            sqlex= sqlInicio+sqlfinal + ");"
            print sqlex
            datos[row[indx]] =row
            return datos



conn = _mssql.connect(
    server=r'FGF',
    user=r'administrador',
    password='Maidenfgf1',
    database='SDE'
)

sqlcmd = """
DECLARE @myval int
EXEC sde.next_rowid 'DBO', 'Locations_point_evw', @myval OUTPUT
SELECT @myval
"""
#res = conn.execute_scalar(sqlcmd)
#print str(res)
#cursor = conn.cursor()
#cursor.execute("""DECLARE @myval int EXEC sde.next_rowid SDE, Hazards_point, @myval OUTPUT SELECT @myval Next RowID""")
#cursor.callproc('FindPerson', ('Jane Doe',))
#cursor.callproc('sde.next_rowid', ('SDE' , 'Hazards_point'))
#for row in cursor:
    #print('row = %r' % (row,))
#conn.commit()
conn.close()

puntosprueba = geodatabaseImsma+os.sep+"Hazards_polygon"
ValoresEntrada(puntosprueba,"FeatureId")