import arcpy,os,sys

FeatuareClass=r"E:\Scripts\EFESIOS.sde\SDE.DBO.Formulario_Ubicacion_Eventos"
GeodatabaseSalida=os.path.dirname(FeatuareClass)
print GeodatabaseSalida
campos = ['SHAPE@XY','longitud','latitud']

edit = arcpy.da.Editor (GeodatabaseSalida)

edit.startEditing (False, False)
edit.startOperation()
with arcpy.da.UpdateCursor(FeatuareClass, campos) as cursor:
    for row in cursor:
        x, y = row[0]
        row[1]=x
        row[2]=y
        cursor.updateRow(row)
edit.stopOperation()
edit.stopEditing("True")