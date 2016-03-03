__author__ = 'fernando.gonzalez'
import arcpy,os, sys

import sys, string,arcgisscripting, os
gp = arcgisscripting.create()
entrada = r"X:\MODELOS DEFINITIVOS\GEODATABASE_V10.0_02_03_2016\10K_Gobernacion\GEODATABASE_VECTORES\CON_ANOTACIONES\10K_V9.2_BOGOTA_CON_ANOTACIONES.mdb"
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
                        gp.AddMessage(fc)
                        gp.AddMessage(" Adicionando Campos al Featuare: " + fc)
                        try:
                            gp.addfield (fc, "CAMBIO", "TEXT","","","2")
                            arcpy.AssignDomainToField_management(fc, "CAMBIO","Dom_Cambios")

                        except:
                            gp.AddMessage(gp.GetMessages(2))
                        try:
                            gp.addfield (fc, "RESPONSABLE", "TEXT","","", "100")
                        except:
                            gp.AddMessage(gp.GetMessages(2))
                        try:
                            gp.addfield (fc, "VIGENCIA", "TEXT","","","2")
                            arcpy.AssignDomainToField_management(fc, "VIGENCIA", "Dom_Vigencia")
                        except:
                            gp.AddMessage(gp.GetMessages(2))
                        try:
                            gp.addfield (fc, "FECHA_MODIFICACION", "DATE")
                        except:
                            gp.AddMessage(gp.GetMessages(2))

                    fc = fcs.next()
          dataset = datasets.next()
