#################
############################
__author__ = 'fernando.gonzalez'
class LicenseError(Exception):
    pass

import arcpy, os, sys, arcinfo
from arcpy.sa import *

DGN = sys.argv[1]
Carpeta= sys.argv[2]
PoligonoArea=sys.argv[3]
Archivo=sys.argv[4]

#######################################################################################
######################################################################
################################################################################
###########################################################################


arcpy.env.overwriteOutput=True
###################

strShape=Carpeta+os.sep+"Shape.shp"
strShape2=Carpeta+os.sep+"Shape2.shp"
strTin=Carpeta+os.sep+"Tin"
strRaster=Carpeta+os.sep+"Raster.tif"
strRasterCorte=Carpeta+os.sep+"RasterCorte.tif"
strSlope=Carpeta+os.sep+"Slope.tif"
strReclass=Carpeta+os.sep+"Reclass.tif"
strPoligono = Carpeta +os.sep+ "Pol.shp"
strEliminate1 = Carpeta+os.sep+ "Eliminate1.shp"
strEliminate2 = Carpeta+os.sep+ "Eliminate2.shp"
strEliminate3 = Carpeta+os.sep+ "Eliminate3.shp"
strEliminate4 = Carpeta+os.sep+ "Eliminate4.shp"
strEliminate5 = Carpeta+os.sep+ "Eliminate5.shp"
strEliminateF = Carpeta+os.sep+ "EliminateF.shp"

RECLASIFICAR = "0.000000 3.000000 1; 3.000001 12.000000 2; 12.000001 9999999999.0000 3"

strDissolve=Carpeta+os.sep+"Dissolve.shp"

def CalcularArea( Feat):
    try:
        arcpy.AddField_management(Feat,"AREA","DOUBLE")
    except:
        pass
    shapeName = arcpy.Describe(Feat).shapeFieldName
    rows = arcpy.UpdateCursor(Feat)
    for row in rows:
        geom=row.getValue(shapeName)
        row.AREA=geom.area
        rows.updateRow(row)
    del row
    del rows

def areaCorte(Feat):
    rows = arcpy.SearchCursor(Feat)
    AreaTotal=0
    for row in rows:
        AreaTotal=AreaTotal+row.AREA
    return AreaTotal




try:
    if arcpy.CheckExtension("3D") == "Available" and arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("3D")
        arcpy.CheckOutExtension("Spatial")
    else:
        # Raise a custom exception
        #
        raise LicenseError

    ##Conversion de DGN a Shape
    arcpy.env.workspace = DGN
    ListaFeat= arcpy.ListFeatureClasses()
    for fc in ListaFeat:
        if fc == "Polyline":
            arcpy.FeatureClassToFeatureClass_conversion(fc,Carpeta,"Shape.shp")
            arcpy.Clip_analysis(strShape,PoligonoArea,strShape2)
    try:
        CalcularArea(PoligonoArea)
        ##Conversion Tin
        arcpy.CreateTin_3d(strTin,"","'"+strShape2+"'" +" Shape.Z masspoints <None>","DELAUNAY")
        ## Tin a Raster
        arcpy.TinRaster_3d(strTin,strRaster,"INT", "LINEAR", "OBSERVATIONS 250")
        ##Cortando raster
        outExtractByMask = ExtractByMask(strRaster, PoligonoArea)
        outExtractByMask.save(strRasterCorte)
        ## Slope Raster
        arcpy.Slope_3d(strRasterCorte, strSlope, "PERCENT_RISE", "1")
        ## Reclasificar Raster
        arcpy.Reclassify_3d (strSlope, "Value", RECLASIFICAR, strReclass, "NODATA")
        ## Raster To Polygon
        arcpy.RasterToPolygon_conversion(strReclass, strPoligono, "NO_SIMPLIFY", "Value")
        ## Unir Poligonos
        arcpy.Dissolve_management(strPoligono, strDissolve, "GRIDCODE", "", "SINGLE_PART")
        ## Calculando Areas
        CalcularArea(strDissolve)
        ## Generalizando
        arcpy.EliminatePolygonPart_management(strDissolve, strEliminate4, "AREA",10000, "", "ANY")
        ## Creando Layer
        arcpy.MakeFeatureLayer_management(strEliminate4, "eliminateLYR")
        ##Seleccion por atributo
        arcpy.SelectLayerByAttribute_management("eliminateLYR", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR", strEliminate1, "LENGTH")
        CalcularArea(strEliminate1)


        arcpy.MakeFeatureLayer_management(strEliminate1, "eliminateLYR2")
        arcpy.SelectLayerByAttribute_management("eliminateLYR2", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR2", strEliminate2, "LENGTH")
        CalcularArea(strEliminate2)

        arcpy.MakeFeatureLayer_management(strEliminate2, "eliminateLYR3")
        arcpy.SelectLayerByAttribute_management("eliminateLYR3", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR3", strEliminate3, "LENGTH")
        CalcularArea(strEliminate3)

        arcpy.MakeFeatureLayer_management(strEliminate3, "eliminateLYR4")
        arcpy.SelectLayerByAttribute_management( "eliminateLYR4", "NEW_SELECTION",""" "AREA"<100000  """)
        arcpy.Eliminate_management ("eliminateLYR4", strEliminate5, "LENGTH")
        arcpy.Dissolve_management(strEliminate5, strEliminateF, "GRIDCODE", "", "MULTI_PART")
        CalcularArea(strEliminateF)




        arcpy.Delete_management("eliminateLYR")
        arcpy.Delete_management("eliminateLYR2")
        arcpy.Delete_management("eliminateLYR3")
        arcpy.Delete_management("eliminateLYR4")

        plano = 0
        ondulado = 0
        montanoso = 0
        AreaTotal2= areaCorte(PoligonoArea)
        rows = arcpy.SearchCursor(strEliminateF)
        for row in rows:
            if row.GRIDCODE==1:
                plano = row.AREA
            elif row.GRIDCODE==2:
                ondulado = row.AREA
            elif row.GRIDCODE==3:
                montanoso = row.AREA
        AreaTotal = plano + ondulado + montanoso

        if AreaTotal== AreaTotal2:
            plano = plano / 10000
            ondulado = ondulado / 10000
            montanoso = montanoso / 10000
        elif AreaTotal< AreaTotal2:
            resto = AreaTotal2 - AreaTotal
            plano = (((plano / AreaTotal) * resto) + plano) / 10000
            ondulado = (((ondulado / AreaTotal) * resto) + ondulado) / 10000
            montanoso = (((montanoso / AreaTotal) * resto) + montanoso) / 10000
        elif AreaTotal > AreaTotal2:
            resto = AreaTotal - AreaTotal2
            plano = (plano - ((plano / AreaTotal) * resto)) / 10000
            ondulado = (ondulado - ((ondulado / AreaTotal) * resto)) / 10000
            montanoso = (montanoso - ((montanoso / AreaTotal) * resto)) / 10000

        planoT=str(round(plano,1))
        onduladoT=str(round(ondulado,1))
        montanosoT=str(round(montanoso,1))
        Fileprj = open (Archivo, "w")
        Fileprj.write("Reporte de areas" + "\n")
        Fileprj.write("Area en Zona Plana: " + planoT+ " Ha" +"\n")
        Fileprj.write("Area en Zona Ondulada: " + onduladoT+ " Ha"+"\n")
        Fileprj.write("Area en Zona Monta?osa: " + montanosoT + " Ha"+"\n")
        Fileprj.close()
    except Exception as ex:
        arcpy.AddError( "Error en el proceso: "+ ex.message)

except LicenseError:
    arcpy.AddError("Se requieren de 3D Analisys y Spatial Analysis para esta Herramienta")
except:
    arcpy.AddError (arcpy.GetMessages(2))
finally:
    # Check in the 3D Analyst extension
    #
    arcpy.CheckInExtension("3D")
    arcpy.CheckInExtension("Spatial")





