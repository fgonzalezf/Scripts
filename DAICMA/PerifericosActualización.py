import arcpy, os, sys

TablaEntrada=r"E:\Scripts\SDE.sde\SDE.dbo.Zonas_asignadas_vista"
TablaSalida=r"E:\Scripts\SDE.sde\SDE.DBO.DAICMA\SDE.DBO.Municipios"
GeodatabaseSalida=r"E:\Scripts\SDE.sde"

CampoIdentificadorEntrada="CODIGODANE"
CampoIdentificadorSalida="COD_DANE"

MapeoCampos={"Estado":"ESTADO_DE_INTERVENCION","Tip_2016":"TIPOLOGIA_2016","Tip_2017":"TIPOLOGIA_2017"}

camposEntrada=[]
camposSalida=[]
camposEntrada.append(CampoIdentificadorEntrada)
camposSalida.append(CampoIdentificadorSalida)

for entrada, salida in MapeoCampos.items():
    camposEntrada.append(entrada)
    camposSalida.append(salida)


print camposSalida
print camposEntrada

edit = arcpy.da.Editor (GeodatabaseSalida)
edit.startEditing ()
edit.startOperation()
with arcpy.da.UpdateCursor(TablaSalida, camposSalida) as cursor:
    for row in cursor:
         print(row[0])
         with arcpy.da.SearchCursor(TablaEntrada, camposEntrada) as cursor2:
            for row2 in cursor2:
                if int(row2[0])==row[0]:
                    row[1]=row2[1]
                    row[2]=row2[2]
                    row[3]=row2[3]
                    cursor.updateRow(row)
edit.stopOperation()
edit.stopEditing("True")





