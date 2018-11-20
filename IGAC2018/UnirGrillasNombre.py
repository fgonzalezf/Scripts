import arcpy, os,sys

Grilla=r"E:\IGAC\Grillas.mdb\Origen_Oeste_Oeste\Planchas_10K_Oeste_Oeste"
Plancha = "PLANCHA"
salida=os.path.dirname(Grilla)+os.sep+"Planchas_25k_Oeste_Oeste"

arcpy.env.workspace=Grilla

def unique_values(table , field):
    try:
        arcpy.AddField_management(table,"Plancha_25K","TEXT","","","255")
    except:
        pass
    fields=[]
    fields.append(field)
    fields.append("Plancha_25K")

    with arcpy.da.UpdateCursor(table, fields) as cursor:
        for row in cursor:
            row[1] = row[0][:-1]
            cursor.updateRow(row)
    arcpy.Dissolve_management(table,salida,"Plancha_25K")



myValues = unique_values(Grilla,Plancha)
print myValues