__author__ = 'fernando.gonzalez'
import arcpy,os, sys

import sys, string,arcgisscripting, os
gp = arcgisscripting.create()
entrada = r"D:\Proyecto\fernando.gonzalez\MODELOS DEFINITIVOS\GEODATABASE_V10.3_08_04_2016\25K\Sin_Anotaciones\25K_08_04_2016_GEODATABASE_CARGUE.mdb"
gp.workspace = entrada

datasets = gp.listdatasets("*", "FEATURE")
dataset = datasets.next()
#arcpy.TableToDomain_management(r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\10K_Gobernacion\Dominios.mdb\Dom_Cambios", "cod", "des", entrada, "Dom_Cambios", "Cambios realizados en edicion")
#arcpy.TableToDomain_management(r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\10K_Gobernacion\Dominios.mdb\Dom_Vigencia", "cod", "des", entrada, "Dom_Vigencia", "Vigencia del elemento")
while dataset:
          gp.workspace = entrada+ "\\"+dataset
          fcs = gp.ListFeatureClasses()
          fc = fcs.next()
          while fc:
                    DSC= gp.describe(fc)
                    if DSC.featureType!="Annotation":
                        #gp.AddMessage(fc)
                        #gp.AddMessage(" Adicionando Campos al Featuare: " + fc)
                        fields=arcpy.ListFields(fc,"*PK_CUE")
                        for field in fields:
                            #arcpy.AddField_management(fc,"PK_CUE_CAMBIO","TEXT","","","50")
                            #arcpy.CreateRelationshipClass_management(entrada+os.sep+"Reporte_Cambios",fc,fc+"Cam_Rel","SIMPLE",)
                            #arcpy.CreateRelationshipClass_management(entrada+os.sep+"Reporte_Cambios", fc, fc+"Cam_Rel","SIMPLE", fc, "Reporte_Cambios", "NONE", "ONE_TO_ONE", "NONE", "PK_CUE_CAMBIO", "PK_CUE_CAMBIO")
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

                    fc = fcs.next()
          dataset = datasets.next()
