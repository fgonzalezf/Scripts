import arcpy,os,sys

datasetEntrada =r"D:\SGC\100K_IGAC.gdb\Mapa_Base_IGAC_100K"
datasetSalida =r"D:\SGC\100KE.gdb\EXCEL"

arcpy.env.workspace=datasetEntrada

ListaFeat= arcpy.ListFeatureClasses()

for fc in ListaFeat:
    estado=0
    count=0
    fields = arcpy.ListFields(fc)
    for field in fields:
        if field.name=="NOMBRE_GEOGRAFICO":
            estado=1
    if estado==1:
            result = arcpy.GetCount_management(fc)
            count = int(result.getOutput(0))
            if count>0:
                print "Exportando..."+fc
                arcpy.FeatureClassToFeatureClass_conversion(datasetEntrada + os.sep + fc,datasetSalida,fc,"""NOMBRE_GEOGRAFICO IS NOT NULL AND NOMBRE_GEOGRAFICO <>''""")


#Borrando Vacios

arcpy.env.workspace=datasetSalida
ListaFeat2= arcpy.ListFeatureClasses()

for fc2 in ListaFeat2:
    result = arcpy.GetCount_management(fc2)
    count = int(result.getOutput(0))
    if count==0:
        print "Borrando..."+fc
        arcpy.Delete_management(fc2)




