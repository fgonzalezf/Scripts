import arcpy, os, sys
from datetime import datetime
Tabla = sys.argv[1]
fields = arcpy.ListFields(Tabla)
validarTabla=0
for field in fields:
    if field.name=="PKCUE_ORIGEN" or field.name=="PROCESO" or field.name=="FECHA_MODIFICACION" or field.name=="PK_CUE_CAMBIO":
        validarTabla+=1
if validarTabla==4:
    cursor = arcpy.UpdateCursor(Tabla)
    for row in cursor:
        try:
            pkcue=row.getValue("PKCUE_ORIGEN")
            fecha=row.getValue("FECHA_MODIFICACION")
            proceso=row.getValue("PROCESO")
            if pkcue!= None and fecha!=None and proceso!=None:
                fechaConvertida = datetime.strftime(fecha, "%Y%m")
                valor=str(int(pkcue))+proceso+"_"+fechaConvertida
                row.setValue("PK_CUE_CAMBIO", valor)
                cursor.updateRow(row)
            else:
                arcpy.AddWarning("OBJECTID: "+str(row.getValue("OBJECTID"))+"  Datos Incompletos..... ")
        except Exception as e:
            arcpy.AddMessage("Error Calculando.." + e.message)

else:
    arcpy.AddError("La tabla Seleccionada no Corresponde A Reporte de Cambios o esta Modificada")


