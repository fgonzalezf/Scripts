import arcpy, os, sys

TablaEntrada=r""
TablaSalida=r""
GeodatabaseSalida=r""

CampoIdentificadorEntrada=""
CampoIdentificadorSalida=""

MapeoCampos={"DANE":"DaneInt","Estado_intervencion":"estado"}

camposEntrada=[]
camposSalida=[]
camposEntrada.append(CampoIdentificadorEntrada)
camposSalida.append(CampoIdentificadorSalida)

for entrada, salida in MapeoCampos.items():
    camposEntrada.append(entrada)
    camposSalida.append(salida)

edit = arcpy.da.Editor (GeodatabaseSalida)
edit.startEditing ()
edit.startOperation()
with arcpy.da.UpdateCursor(TablaSalida, camposSalida) as cursor:
    for row in cursor:
         with arcpy.da.SearchCursor(TablaEntrada, camposEntrada) as cursor2:
            for row2 in cursor2:
                if row2[0]==row[0]:
                    row2[1]=row[1]
                    row2[2]=row[2]
                    row2[3]=row[3]
                    row2[4]=row[4]
                    cursor2.updateRow(row2)
edit.stopOperation()
edit.stopEditing("True")





