import arcpy, os,sys

reload(sys)
sys.setdefaultencoding('latin1')

TablaEntrada=r'C:\Users\fernando.gonzalez\Documents\PlanView\PLANVIEW\PLANVIEW.mdb'
TablaEntradaFin = os.path.join(TablaEntrada,"VSIG_Proyectos")
TablaSalida =r"C:\Users\fernando.gonzalez\Documents\PlanView\PLANVIEW\PLANVIEW.mdb\prueba"
arcpy.env.workspace=TablaEntrada
#ListaCamposEntrada=arcpy.ListFields(TablaEntrada)
#ListaCamposSalida= arcpy.ListFields(TablaSalida)

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})
fields=["ProjectKey",
        "SGCCode",
        "ProjectName",
        "ScheduleStart",
        "ScheduleFinish",
        "PercentComplete",
        "Productos",
        "Tipo",
        "Municipio",
        "Descripcion",
        "Objetivo",
        "tproductosoficializar",
        "cobertura",
        "Plancha100K",
        "EnfoqueEstrategico",
        "LineaTematica",
        "URL_Shape"]
unicos = unique_values(TablaEntradaFin,"SGCCode")
cursorIns = arcpy.da.InsertCursor(TablaSalida,fields)
for valor in unicos:
    expression = arcpy.AddFieldDelimiters(TablaEntradaFin, "SGCCode") + "= '"+ valor +"'"
    rowIns=[]
    with arcpy.da.SearchCursor(TablaEntradaFin, fields, where_clause=expression) as cursor:
        estado=0
        for row in cursor:
            if estado==0:
                for i in range(len(row)):
                    rowIns.append([])
            for i in range(len(row)):
                if str(row[i]) not in rowIns[i]:
                    rowIns[i].append(str(row[i]))
            estado=1
    #Conversion en tupla
    campIn=[]
    for val in rowIns:
        temStr=""
        for valint in val:
            temStr=temStr+valint
        campIn.append(temStr)
    rowFin=tuple(campIn)
    print rowFin
    cursorIns.insertRow(rowFin)



#cursor = arcpy.da.InsertCursor(TablaSalida, fields)
print unique_values(TablaEntradaFin,"SGCCode")



print "Terminado"

