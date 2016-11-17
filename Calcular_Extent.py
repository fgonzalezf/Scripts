import arcpy, os, sys

FeatEntrada = r"C:\Users\fernando.gonzalez\Documents\PlanView\PlanVie2\PLANVIEW.mdb\Poligonos"
TablaSalida = r"C:\Users\fernando.gonzalez\Documents\PlanView\PlanVie2\PLANVIEW.mdb\prueba"

CamposEntrada=["SGCCode","SHAPE@"]
CamposSalida=["SGCCode","LatMin","LatMax","LogMin","LogMax"]

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})


with arcpy.da.SearchCursor(FeatEntrada,CamposEntrada) as cursor:
    try:
        for row in cursor:
            with arcpy.da.UpdateCursor(TablaSalida, CamposSalida) as cursorup:
                for rowup in cursorup:
                    if row[0]==rowup[0]:
                        arcpy.AddMessage("Actualizando..."+ str(row[0]))
                        rowup[1]=row[1].extent.XMin
                        rowup[2]=row[1].extent.XMax
                        rowup[3]=row[1].extent.YMin
                        rowup[4]=row[1].extent.YMax
                        cursorup.updateRow(rowup)
    except:
        arcpy.AddMessage("Error Actualizando Tabla")