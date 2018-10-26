__author__ = 'fgonzalezf'

import arcpy, os,sys
reload(sys)
arcpy.env.overwriteOutput=True
sys.setdefaultencoding("utf-8")
FeatEntrada=r"C:\Users\fgonzalezf\Documents\Amenaza_Volcanica_Galeras_capas\Fenomenos\Prueba.gdb\F40_UC_UNICRO"
Tabla=r"C:\Users\fgonzalezf\Documents\Amenaza_Volcanica_Galeras_capas\Fenomenos\Prueba.gdb\Unidades_Atlas"
arcpy.env.overwriteOutput=True
try:
    arcpy.CreateTable_management(os.path.dirname(Tabla),os.path.basename(Tabla))
except:
    pass



Fields = arcpy.ListFields(FeatEntrada)
Campos=[]
for field in Fields:
    #Encabezados

    if str(field.name)!='SHAPE' and str(field.name)!='OBJECTID' and str(field.name)!='OBJECTID_1'and str(field.name)!='SHAPE.AREA'and str(field.name)!='OVERRIDE' and str(field.name)!='RULEID'and str(field.name)!='SHAPE.LEN' :
        Campos.append(str(field.name))
        if field.type=="String":
            arcpy.AddField_management(Tabla,field.name,"TEXT","","",field.length)
        elif field.type=="Integer":
            arcpy.AddField_management(Tabla,field.name,"LONG")
        elif field.type=="Double":
            arcpy.AddField_management(Tabla,field.name,"DOUBLE")
        elif field.type=="SmallInteger":
            arcpy.AddField_management(Tabla,field.name,"SHORT")
        elif field.type=="Date":
            arcpy.AddField_management(Tabla,field.name,"DATE")

#Encabezado Extent

desc= arcpy.Describe(FeatEntrada)
if desc.shapeType!="Point":
    arcpy.AddField_management(Tabla,"Xmin","DOUBLE")
    arcpy.AddField_management(Tabla,"Xmax","DOUBLE")
    arcpy.AddField_management(Tabla,"Ymin","DOUBLE")
    arcpy.AddField_management(Tabla,"Ymax","DOUBLE")
else:
    arcpy.AddField_management(Tabla,"Xmin","DOUBLE")
    arcpy.AddField_management(Tabla,"Ymin","DOUBLE")

Campos2=[]
for campo in Campos:
    Campos2.append(campo)
if desc.shapeType!="Point":
    Campos2.append("Xmin")
    Campos2.append("Xmax")
    Campos2.append("Ymin")
    Campos2.append("Ymax")
else:
    Campos2.append("Xmin")
    Campos2.append("Ymin")



print Campos
print Campos2


#Filesal.write(fc + "\n")
X=0
cursorins = arcpy.da.InsertCursor(Tabla,Campos2)
Campos.append("SHAPE@")
with arcpy.da.SearchCursor(FeatEntrada,Campos) as cursor:
    try:
        for row in cursor:
            X=X+1
            print "Elemento: "+ str(X)
            if row[len(Campos)-1].extent != None:
                rowins=[]
                for x in range(0, len(Campos)-1):
                    #print x
                    #print str(row[x])
                    rowins.append(row[x])
                if desc.shapeType!="Point":
                    rowins.append(row[len(Campos)-1].extent.XMin)
                    rowins.append(row[len(Campos)-1].extent.XMax)
                    rowins.append(row[len(Campos)-1].extent.YMin)
                    rowins.append(row[len(Campos)-1].extent.YMax)
                else:
                    rowins.append(row[len(Campos)-1].extent.XMin)
                    rowins.append(row[len(Campos)-1].extent.YMin)

                print len(rowins)
                print rowins
                cursorins.insertRow(rowins)
    except Exception as e:
        arcpy.AddMessage(e.message)




