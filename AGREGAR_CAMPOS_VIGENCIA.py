__author__ = 'fernando.gonzalez'
import arcpy,os, sys

import sys, string, os

entrada = r"D:\Proyecto\EDICION\INTEGRADAS_25K_BORRAR\Back_Up_25K_PROYECTADA.gdb"
arcpy.env.workspace= entrada

datasets = arcpy.arcpy.ListDatasets("*", "FEATURE")

#arcpy.TableToDomain_management(r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\10K_Gobernacion\Dominios.mdb\Dom_Cambios", "cod", "des", entrada, "Dom_Cambios", "Cambios realizados en edicion")
#arcpy.TableToDomain_management(r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\10K_Gobernacion\Dominios.mdb\Dom_Vigencia", "cod", "des", entrada, "Dom_Vigencia", "Vigencia del elemento")
for dataset in datasets:
          arcpy.env.workspace = entrada+ os.sep +dataset
          fcs = arcpy.ListFeatureClasses()

          for fc in fcs:

                    DSC= arcpy.Describe(fc)
                    if DSC.featureType!="Annotation":
                        arcpy.AddMessage(fc)
                        arcpy.AddMessage(" Relaciones: " + fc)
                        fields=arcpy.ListFields(fc,"*")
                        for field in fields:
                            if field.name=="PK_CUE_CAMBIO":
                            #arcpy.AddField_management(fc,"HOJA","TEXT","","","20")
                            #arcpy.CreateRelationshipClass_management(entrada+os.sep+"Reporte_Cambios",fc,fc+"Cam_Rel","SIMPLE",)
                                try:
                                    arcpy.CreateRelationshipClass_management(entrada+os.sep+"Reporte_Cambios", fc, fc+"_Cam_Rel","SIMPLE", fc, "Reporte_Cambios", "NONE", "ONE_TO_ONE", "NONE", "PK_CUE_CAMBIO", "PK_CUE_CAMBIO")
                                except:
                                    pass
                        print fc
                        #arcpy.AddField_management(fc,"PLANCHA","TEXT","","","20")
                        # try:
                        #     gp.addfield (fc, "CAMBIO", "TEXT","","","2")
                        #     arcpy.AssignDomainToField_management(fc, "CAMBIO","Dom_Cambios")
                        #
                        # except:
                        #     gp.AddMessage(gp.GetMessages(2))
                        # try:
                        #     gp.addfield (fc, "RESPONSABLE", "TEXT","","", "100")
                        # except:
                        #     gp.AddMessage(gp.GetMessages(2))
                        # try:
                        #     gp.addfield (fc, "VIGENCIA", "TEXT","","","2")
                        #     arcpy.AssignDomainToField_management(fc, "VIGENCIA", "Dom_Vigencia")
                        # except:
                        #     gp.AddMessage(gp.GetMessages(2))
                        # try:
                        #     gp.addfield (fc, "FECHA_MODIFICACION", "DATE")
                        # except:
                        #     gp.AddMessage(gp.GetMessages(2))
