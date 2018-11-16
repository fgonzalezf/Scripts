import arcpy, os, sys

Geodatabase = r"C:\Users\Desarrollo\Downloads\Nevado huila.mdb"
carpetasalida=r"C:\Users\Desarrollo\Downloads"

Tablas =[]

Tablas.append(Geodatabase+os.sep+"ucg_p_polygon_Magna")


for tabla in Tablas:
    try:
        arcpy.AddField_management(tabla, "Xmin","DOUBLE","","","","Xmin Longitud Minima")
        arcpy.AddField_management(tabla, "Xmax", "DOUBLE", "", "", "", "Xmax Longitud Maxima")
        arcpy.AddField_management(tabla, "Ymin", "DOUBLE", "", "", "", "Ymin Latitud Minima")
        arcpy.AddField_management(tabla, "Ymax", "DOUBLE", "", "", "", "Ymax LatitudMaxima")
    except Exception as e:
        print  "campos Ya creados..." + e.message

    edit = arcpy.da.Editor(Geodatabase)
    edit.startEditing()
    edit.startOperation()

    camposExtent= ['SHAPE@',"Xmin","Xmax","Ymin","Ymax"]

    with arcpy.da.UpdateCursor(tabla, camposExtent) as cursor:
        x=0
        for row in cursor:
            x+=1
            row[1]=row[0].extent.XMin
            row[2] = row[0].extent.XMax
            row[3] = row[0].extent.YMin
            row[4]=row[0].extent.YMax
            arcpy.AddMessage(str(x)+ "...")
            cursor.updateRow(row)
    edit.stopOperation()
    edit.stopEditing("True")
    arcpy.TableToExcel_conversion(tabla,carpetasalida+os.sep+tabla)

