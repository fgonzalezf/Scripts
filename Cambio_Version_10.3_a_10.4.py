import arcpy, os,sys
#Geodatabase =r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\PRUEBAS_PLANCHA\92IVA.mdb"
#Hoja="92IVA_R"
Geodatabase=sys.argv[1]

arcpy.env.workspace=Geodatabase
ListaDatasets = arcpy.ListDatasets()
for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase +os.sep+ dataset
    ListaFeatures= arcpy.ListFeatureClasses()
    if dataset=="Puntos_de_Control":
        Topologia=Geodatabase +os.sep+ dataset+os.sep+"Puntos_de_Control_Topology"
        for fc in ListaFeatures:
            if fc=="Punto_Geodesico" or fc=="Punto_Geodesico_Anot" or fc=="Punto_Nivelacion" or fc=="Punto_Nivelacion_Anot" or fc=="Punto_Topografico" or fc=="Punto_Topografico_Anot":
                try:
                    Dsc=arcpy.Describe(fc)
                    if Dsc.featureType != "Annotation":
                        arcpy.RemoveFeatureClassFromTopology_management(Topologia,fc)
                except Exception as e:
                    arcpy.AddMessage("Error eliminado Featuare de Topologia "+ e.message)
                try:
                    arcpy.Delete_management(fc)
                except Exception as e:
                    arcpy.AddMessage("Error eliminado FeatuareClass "+ e.message)
            elif fc=="Punto_Fotocontrol":
                arcpy.RemoveFeatureClassFromTopology_management(Topologia,fc)
                nuevo=arcpy.Rename_management(fc,"Punto_Control_Terrestre")
                arcpy.AlterAliasName(nuevo,"Punto_Control_Terrestre")
                nuevo2=arcpy.Rename_management(fc+"_Anot","Punto_Control_Terrestre_Anot")
                arcpy.AlterAliasName(nuevo2,"Punto_Control_Terrestre_Anot")

    elif dataset=="Superficies_Agua":
        Topologia=Geodatabase +os.sep+ dataset+os.sep+"Superficies_Agua_Topology"
        for fc in ListaFeatures:
            if fc=="Linea_Costera":
                arcpy.RemoveFeatureClassFromTopology_management(Topologia,fc)
                nuevo=arcpy.Rename_management(fc,"Linea_Mar")
                arcpy.AlterAliasName(nuevo,"Linea_Mar")
                arcpy.AddFeatureClassToTopology_management(Topologia,nuevo)
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Overlap (Line)",nuevo,"",Geodatabase +os.sep+ dataset+os.sep+"Drenaje_Sencillo","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Overlap (Line)",nuevo,"",Geodatabase +os.sep+ dataset+os.sep+"Madrevieja_L","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Overlap (Line)",nuevo,"",Geodatabase +os.sep+ dataset+os.sep+"Raudal_Rapido","", )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Intersect (Line)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Have Dangles (Line)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Have Pseudo-Nodes (Line)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Self-Overlap (Line)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Self-Intersect (Line))",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Be Single Part (Line)",nuevo,"","","" )

    elif dataset=="Indice_Mapas":
        Topologia=Geodatabase +os.sep+ dataset+os.sep+"Indice_Mapas_Topology"
        for fc in ListaFeatures:
            if fc=="IndEscala":
                arcpy.RemoveFeatureClassFromTopology_management(Topologia,fc)
                nuevo=arcpy.Rename_management(fc,"Indice_Hoja_Cartografica")
                arcpy.AlterAliasName(nuevo,"Indice_Hoja_Cartografica")
                arcpy.AddFeatureClassToTopology_management(Topologia,nuevo)
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Overlap (Area)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Have Gaps (Area)",nuevo,"","","" )

    elif dataset=="Indice_Mapas":
        Topologia=Geodatabase +os.sep+ dataset+os.sep+"Indice_Mapas_Topology"
        for fc in ListaFeatures:
            if fc=="IndEscala":
                arcpy.RemoveFeatureClassFromTopology_management(Topologia,fc)
                nuevo=arcpy.Rename_management(fc,"Indice_Hoja_Cartografica")
                arcpy.AlterAliasName(nuevo,"Indice_Hoja_Cartografica")
                arcpy.AddFeatureClassToTopology_management(Topologia,nuevo)
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Overlap (Area)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Have Gaps (Area)",nuevo,"","","" )
                arcpy.AddRuleToTopology_management(Topologia,"Must Not Have Gaps (Area)",nuevo,"","","" )



