import arcpy, os, sys

#Curvas=r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\Curvas\Prueba_Curvas\Prueba2.gdb\Curvas"
#Indices=r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\Curvas\Prueba_Curvas\Prueba2.gdb\Indice"
#Carpeta=r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\Curvas\Prueba_Curvas"

Curvas=sys.argv[1]
Indices=sys.argv[2]
Carpeta=sys.argv[3]

arcpy.env.overwriteOutput=True
cursor = arcpy.SearchCursor(Indices)


for row in cursor:
        try:
            arcpy.AddMessage("Creando Curvas " + str(row.getValue("PLANCHA")))
            arcpy.MakeFeatureLayer_management(Indices,"LayerIndice",'''PLANCHA = ''' + "'" +row.getValue("PLANCHA")+ "'")
            arcpy.MakeFeatureLayer_management(Curvas,"LayerCurvas")
            LayerCurvas=arcpy.SelectLayerByLocation_management("LayerCurvas",'intersect',"LayerIndice","-1 Meters","NEW_SELECTION")
            Tin= arcpy.CreateTin_3d(Carpeta+os.sep+"TinTemp",r"C:\Users\fernando.gonzalez\AppData\Roaming\ESRI\Desktop10.3\ArcMap\Coordinate Systems\MAGNA Colombia Bogota.prj","LayerCurvas"+" TALT masspoints")
            Raster=arcpy.TinRaster_3d(Tin, Carpeta+ os.sep+"raster.img", "FLOAT", "NATURAL_NEIGHBORS", "CELLSIZE 5", 1)
            arcpy.Contour_3d(Carpeta+ os.sep+"raster.img",Carpeta+ os.sep+str(row.getValue("PLANCHA"))+"_"+"curvas.shp",25,0)

            arcpy.Delete_management("LayerIndice")
            arcpy.Delete_management("LayerCurvas")
            arcpy.Delete_management(Tin)
            arcpy.Delete_management(Raster)
        except:
            pass

del cursor, row


