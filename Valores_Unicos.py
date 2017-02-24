__author__ = 'fgonzalezf'
import arcpy, os,sys

Entrada1=sys.argv[1]
Entrada2=sys.argv[2]
#Salida=r"Join"

FieldsStr=sys.argv[3]
FieldUnico=sys.argv[4]

Fields=FieldsStr.split(";")

arcpy.env.overwriteOutput=True
#Join spatial
Join=os.path.dirname(Entrada1)+os.sep+"JoinTemporal"
arcpy.SpatialJoin_analysis(Entrada1,Entrada2,os.path.dirname(Entrada1)+os.sep+"JoinTemporal","JOIN_ONE_TO_MANY","KEEP_COMMON","","INTERSECT","-100 METERS")
TablaSalida= os.path.dirname(Entrada2)+os.sep+os.path.basename(Entrada1)+"_"+os.path.basename(Entrada2)
print TablaSalida
print os.path.basename(Entrada1)+"_"+os.sep+os.path.basename(Entrada2)
arcpy.CreateTable_management(os.path.dirname(Entrada2),os.path.basename(Entrada1)+"_"+os.path.basename(Entrada2))
for fieldname in Fields:
    arcpy.AddField_management(TablaSalida,fieldname,"TEXT","","","4000",fieldname)

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

ValoresUnicos = unique_values(Join, FieldUnico)
cursor2 = arcpy.da.InsertCursor(TablaSalida,(Fields))
for valor in ValoresUnicos:
    with arcpy.da.SearchCursor(Join, (Fields)) as cursor:
        print valor
        Y=""
        for row in cursor:
            if row[0]==valor:
                Y=Y+","+str(row[1])
        cursor2.insertRow((valor,Y[1:]))#Remover la primera ,
del cursor
del cursor2
del row

arcpy.JoinField_management(Entrada1,Fields[0],TablaSalida,Fields[0],[Fields[1]])

try:
    arcpy.Delete_management(Join)
    arcpy.Delete_management(TablaSalida)
except:
    print "Error Borrando Capas"





