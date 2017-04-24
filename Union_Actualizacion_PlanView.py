import arcpy, os,sys

reload(sys)
sys.setdefaultencoding('latin1')

TablaEntrada=r'C:\Users\fernando.gonzalez\Documents\PlanView\PlanVie2\PLANVIEW.mdb'
TablaEntradaFin = os.path.join(TablaEntrada,"VSIG_Proyectos")
TablaSalida =r"C:\Users\fernando.gonzalez\Documents\PlanView\PlanVie2\PLANVIEW.mdb\prueba"
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
unicosSalida = unique_values(TablaSalida,"SGCCode")
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
                if row[i] not in rowIns[i]:
                    rowIns[i].append(row[i])
            estado=1
    #Conversion en tupla
    campIn=[]
    for val in rowIns:
        temStr=""
        valfin=None
        for valint in val:
            if isinstance(valint, basestring):
                temStr=temStr+valint+";"
            else:
                valfin= valint
        if temStr!="":
            campIn.append(temStr[:-1])
        else:
            campIn.append(valfin)
    rowFin=tuple(campIn)
    if valor in unicosSalida:
        expressionSal = arcpy.AddFieldDelimiters(TablaEntradaFin, "SGCCode") + "= '"+ valor +"'"
        with arcpy.da.UpdateCursor(TablaSalida, fields ,expressionSal) as cursor2:
            for rowS in cursor2:
                try:
                    for i in range(len(rowS)):
                        rowS[i]=rowFin[i]
                    cursor2.updateRow(rowS)
                except Exception as ex:
                    print "Error Actualizando Fila " + valor + "...." +ex.message

    else:
        try:
            print rowFin
            cursorIns.insertRow(rowFin)
        except Exception as ex:
                    print "Error Insertando Fila " + valor + "...." +ex.message

print "Terminado"

