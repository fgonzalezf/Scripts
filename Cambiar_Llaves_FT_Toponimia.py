#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import arcpy, os, sys
reload(sys)
sys.setdefaultencoding("iso-8859-1")
Carpeta =sys.argv[1]
#Carpeta =r"X:\PRUEBAS\Cambio_Llave_toponimia\Toponimia\2011"
arcpy.env.workspace = Carpeta
ListaCarpetas = arcpy.ListWorkspaces()
for geodatabase in ListaCarpetas:
    try:
        arcpy.AddMessage(geodatabase)
        arcpy.env.workspace = geodatabase
        desc = arcpy.Describe(geodatabase)
        listaDominios= desc.domains
        for domain in listaDominios:
            print domain
            if domain =="Dom_Proceso":
                try:
                    arcpy.DeleteCodedValueFromDomain_management(geodatabase,domain,"_MB")
                except Exception as e:
                    print e.message
                    pass
        listaTablas= arcpy.ListTables()
        for tabla in listaTablas:
            print tabla
            result = arcpy.GetCount_management(tabla)
            count = int(result.getOutput(0))
            if count>0:
                cursor = arcpy.UpdateCursor(tabla)
                for row in cursor:
                    if row.getValue("PROCESO")=="_AC" or row.getValue("PROCESO")=="ACTUALIZACIÓN":
                        row.setValue("PROCESO", "_CC")
                        row.setValue("FT_PLANCHA",str(row.getValue("FT_PLANCHA")).replace("_AC_","_CC_"))
                        cursor.updateRow(row)
                    if row.getValue("PROCESO")=="_MB" or row.getValue("PROCESO")=="MANTENIMIENTO DE BASES":
                        row.setValue("PROCESO", "_CC")
                        row.setValue("FT_PLANCHA",str(row.getValue("FT_PLANCHA")).replace("_MB_","_CC_"))
                        cursor.updateRow(row)
                del cursor
        arcpy.env.workspace = geodatabase
        ListaFeatuares= arcpy.ListFeatureClasses()
        for fc in ListaFeatuares:
            if fc=="FT_Indice_Mapas":
                cursor = arcpy.UpdateCursor(fc)
                for row in cursor:
                    row.setValue("FT_PLANCHA",str(row.getValue("FT_PLANCHA")).replace("_AC_","_CC_").replace("_MB_","_CC_"))
                    cursor.updateRow(row)
                del cursor
    except Exception as e:
        arcpy.AddMessage("Error en la GDB: "+ geodatabase+ " "+e.message)




