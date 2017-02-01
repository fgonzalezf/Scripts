import arcpy, os, sys

class LicenseError(Exception):
    pass

carpetaRaster = r"C:\Users\fgonzalezf\Documents\TALLERES\bccrBcm2_2050\bccrBcm2_2050"
carpetaTxt=r"C:\Users\fgonzalezf\Documents\TALLERES\bccrBcm2_2050\TXT"
arcpy.env.workspace= carpetaRaster
arcpy.env.overwriteOutput= True

try:
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:            # raise a custom exception
        raise LicenseError

    ListaRaster= arcpy.ListRasters()
    ArchivoTXT = open (carpetaTxt+os.sep+"valores"+".txt", "w")
    for raster in ListaRaster:
            if (raster.find(".asc")!=-1):
                print raster
                arcpy.ASCIIToRaster_conversion(carpetaRaster+os.sep+raster, carpetaRaster+os.sep+raster.replace(".asc",".tif"), "INTEGER")
                rasterResultante = carpetaRaster+ os.sep+ raster.replace(".asc",".tif")
                elevSTDResult = arcpy.GetRasterProperties_management(rasterResultante, "MAXIMUM")
                #Get the elevation standard deviation value from geoprocessing result object
                Maximo = elevSTDResult.getOutput(0)
                ArchivoTXT.write("Nombre raster: "+ raster + "..." + "Valor Maximo: " + str(Maximo)+"\n")

except LicenseError:
        print("Spatial Analyst No tiene Licencia")
except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))





