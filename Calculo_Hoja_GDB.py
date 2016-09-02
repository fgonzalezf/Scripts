import arcpy, os,sys
#Geodatabase =r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\PRUEBAS_PLANCHA\92IVA.mdb"
#Hoja="92IVA_R"
Geodatabase=sys.argv[1]
Hoja=sys.argv[2]
arcpy.env.workspace=Geodatabase
ListaDatasets = arcpy.ListDatasets("*","Feature")
for dataset in ListaDatasets:
    arcpy.env.workspace=Geodatabase +os.sep+ dataset
    ListaFeatures= arcpy.ListFeatureClasses()
    for fc in ListaFeatures:
        Conteo = int(arcpy.GetCount_management(fc).getOutput(0))
        if Conteo>0:
            ListaCampos= arcpy.ListFields(fc)
            for campo in ListaCampos:
                if campo.name=="HOJA" or campo.name=="PLANCHA":
                    Cursor = arcpy.UpdateCursor(fc)
                    arcpy.AddMessage("Actualizando FetuareClass: "+fc)
                    print("Actualizando FetuareClass: "+fc+ "...."+ campo.name)
                    for row in Cursor:
                        try:
                            row.setValue(campo.name, Hoja)
                            Cursor.updateRow(row)
                        except Exception as e:
                            arcpy.AddWarning("Error actualizando OBJECTID: " + str(row.getValue("OBJECTID"))+"..."+ e.message)
                    del Cursor
                    del row

arcpy.env.workspace=Geodatabase
ListaTablas= arcpy.ListTables()
for tabla in ListaTablas:
     Conteo = int(arcpy.GetCount_management(tabla).getOutput(0))
     if Conteo>0:
         ListaCampos= arcpy.ListFields(tabla)
         for campo in ListaCampos:
             if campo.name=="HOJA" or campo.name=="PLANCHA":
                 Cursor = arcpy.UpdateCursor(tabla)
                 arcpy.AddMessage("Actualizando Tabla: "+tabla)
                 print("Actualizando FetuareClass: "+tabla+ "...."+ campo.name)
                 for row in Cursor:
                     try:
                         row.setValue(campo.name, Hoja)
                         Cursor.updateRow(row)
                     except Exception as e:
                         arcpy.AddWarning("Error actualizando OBJECTID: " + str(row.getValue("OBJECTID"))+"..."+ e.message)
                 del Cursor
                 del row




