import arcpy, os, sys

Geodatabase = r"C:\Users\Equipo\Documents\SGC\EPIS_Pruebas.gdb"

Tablas =[]

Tablas.append(Geodatabase+os.sep+"EPIS"+os.sep+"SISMICA2D_EPIS_SGC")
Tablas.append(Geodatabase+os.sep+"EPIS"+os.sep+"SISMICA3D_EPIS_SGC")
Tablas.append(Geodatabase+os.sep+"EPIS"+os.sep+"POLIPROGRAMAS_2D")

for tabla in Tablas:
    try:
        arcpy.AddField_management(tabla, "Xmin","DOUBLE","","","","Xmin Longitud Minima")
        arcpy.AddField_management(tabla, "Xmax", "DOUBLE", "", "", "", "Xmax Longitud Maxima")
        arcpy.AddField_management(tabla, "Ymin", "DOUBLE", "", "", "", "Ymin Latitud Minima")
        arcpy.AddField_management(tabla, "Ymax", "DOUBLE", "", "", "", "Ymax LatitudMaxima")
    except Exception as e:
        print ( "campos Ya creados..." + e.message())

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
            print (str(x)+ "...")
            cursor.updateRow(row)
    edit.stopOperation()
    edit.stopEditing("True")

