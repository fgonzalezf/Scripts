import arcpy,os, sys

arcpy.env.workspace = r"D:\BackUpMisDocumentos\Cuenta de Cobro\Cuenta_de_Cobro_Enero_2018\GDB\Bk_GDB.gdb\DAICMA"

fcList = arcpy.ListFeatureClasses()


for fc in fcList:
    print fc
    if fc!="Colombia" and fc!="Sectores" and fc!="Eventos" and fc!="Municipios" and fc!="Departamento" and fc!="Zonas"and fc!="Estudios_No_Tecnicos_Punto" and fc!="Estudios_Tecnicos_Punto":
        fields=[]
        if fc=="Estudios_Tecnicos" or fc=="Areas_Despejadas" :
            fields=["SHAPE@","FeatureID","hazreduc_localid"]
        elif fc=="Estudios_No_Tecnicos":
            fields=["SHAPE@","FeatureID","hazreduc_localid"]
        else:
            fields=["SHAPE@","FeatureID","hazard_localid"]
        with arcpy.da.SearchCursor(fc, fields) as cursor:
            for row in cursor:

                geometry = row[0]

                if geometry.isMultipart == True:
                    print "FeatureID: "+";"+row[1]+";"+"hazard_localid: "+ row[2]

                    partnum = 0
                    while partnum < geometry.partCount:
                        part = geometry.getPart(partnum)
                        #print arcpy.Polygon(part).pointCount
                        partnum += 1