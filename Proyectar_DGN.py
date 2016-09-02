import arcpy, os,sys

DGNEntrada= r"X:\PRUEBAS\CAROLINA\Proyeccion\ANT_10000_OESTE_105ID3_V7.dgn"
DGNSalida= r"X:\PRUEBAS\CAROLINA\Proyeccion\105ID3_BOGOTA.dgn"

inCoordinateSystem=r"C:\Users\fernando.gonzalez\AppData\Roaming\ESRI\Desktop10.3\ArcMap\Coordinate Systems\MAGNA Colombia Oeste.prj"
outCoordinateSystem=r"C:\Users\fernando.gonzalez\AppData\Roaming\ESRI\Desktop10.3\ArcMap\Coordinate Systems\MAGNA Colombia Bogota.prj"

semilla3d=r"c:\arcgis\desktop10.3\ArcToolbox\Templates\template3d.dgn"

arcpy.env.workspace = DGNEntrada
arcpy.env.overwriteOutput=True
ListaFeatuares= arcpy.ListFeatureClasses()

def BorrarCampos(Feat):
    ListaCampos = arcpy.ListFields(Feat)
    listaBorrar=[]
    for field in ListaCampos:
        if field.name !="FID" and field.name !="Shape" and field.name !="Layer":
            listaBorrar.append(field.name)

    arcpy.DeleteField_management(Feat,listaBorrar)

for fcDGN in ListaFeatuares:
    Describe = arcpy.Describe(fcDGN)
    print fcDGN
    if Describe.shapeType=="Point" and Describe.featureType=="Simple":
        puntos= os.path.dirname(DGNSalida)+ os.sep+"Puntos.shp"
        arcpy.FeatureClassToFeatureClass_conversion(fcDGN,os.path.dirname(DGNSalida),"Puntos.shp")
        arcpy.DefineProjection_management(puntos,inCoordinateSystem)
        puntosDef= os.path.dirname(DGNSalida)+ os.sep+"PuntosDef.shp"
        arcpy.Project_management(puntos,puntosDef,outCoordinateSystem,"")
        BorrarCampos(puntosDef)
        arcpy.ExportCAD_conversion(puntosDef,"DGN_V8",DGNSalida,"IGNORE_FILENAMES_IN_TABLES","APPEND_TO_EXISTING_FILES",semilla3d)
        arcpy.Delete_management(puntos)
        arcpy.Delete_management(puntosDef)
    elif Describe.shapeType=="Polyline"and Describe.featureType=="Simple":
        lineas= os.path.dirname(DGNSalida)+ os.sep+"Lineas.shp"
        arcpy.FeatureClassToFeatureClass_conversion(fcDGN,os.path.dirname(DGNSalida),"Lineas.shp")
        arcpy.DefineProjection_management(lineas,inCoordinateSystem)
        lineasDef= os.path.dirname(DGNSalida)+ os.sep+"LineasDef.shp"
        arcpy.Project_management(lineas,lineasDef,outCoordinateSystem,"")
        BorrarCampos(lineasDef)
        arcpy.ExportCAD_conversion(lineasDef,"DGN_V8",DGNSalida,"IGNORE_FILENAMES_IN_TABLES","APPEND_TO_EXISTING_FILES",semilla3d)
        arcpy.Delete_management(lineas)
        arcpy.Delete_management(lineasDef)
    elif Describe.shapeType=="Polygon"and Describe.featureType=="Simple":
        poligonos= os.path.dirname(DGNSalida)+ os.sep+"Poligonos.shp"
        arcpy.FeatureClassToFeatureClass_conversion(fcDGN,os.path.dirname(DGNSalida),"Poligonos.shp")
        arcpy.DefineProjection_management(poligonos,inCoordinateSystem)
        poligonosDef= os.path.dirname(DGNSalida)+ os.sep+"PoligonosDef.shp"
        arcpy.Project_management(poligonos,poligonosDef,outCoordinateSystem,"")
        BorrarCampos(poligonosDef)
        arcpy.ExportCAD_conversion(poligonosDef,"DGN_V8",DGNSalida,"IGNORE_FILENAMES_IN_TABLES","APPEND_TO_EXISTING_FILES",semilla3d)
        arcpy.Delete_management(poligonos)
        arcpy.Delete_management(poligonosDef)


