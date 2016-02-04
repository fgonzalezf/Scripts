__author__ = 'fernando.gonzalez'

import arcpy,os,sys

DGN=r'X:\PRUEBAS\INGRID\ANT_10000_OESTE_105ID2_COMP_V7.dgn'
Geodatabase=r'X:\PRUEBAS\INGRID\ANT_10000_OESTE_105ID2_COMP_V7.mdb'
SistemaRef= arcpy.CreateSpatialReference_management(r"C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\National Grids\South America\MAGNA Colombia Bogota.prj")
arcpy.env.workspace=DGN
arcpy.CreatePersonalGDB_management(os.path.dirname(Geodatabase),os.path.basename(Geodatabase))
arcpy.CreateFeatureDataset_management(Geodatabase,"DGN",SistemaRef)
ListaFeat= arcpy.ListFeatureClasses()


for fc in ListaFeat:
    try:
        if fc=="Point" or fc =="Polygon" or fc=="Polyline":
            salida=arcpy.FeatureClassToFeatureClass_conversion(fc,Geodatabase+os.sep+"DGN",fc,"",)
            fields =arcpy.ListFields(salida)
            print fc
            for field in fields:
                print field.name
                if field.name!="OBJECTID" and field.name!="Level_" and field.name!="Shape_Length" and field.name!="Shape_Area" and field.name!="Shape" and field.name!="Layer":
                    arcpy.DeleteField_management(salida,field.name)
                    print field.name
    except:
        arcpy.AddMessage("Error"+ fc)

