# -*- coding: utf-8 -*-
import zipfile
import sys
import os
import glob
import datetime

import arcpy
FeatureClass=r"D:\SGC\EPIS\epis_17_11.mdb\EPIS\POZOS_EPIS_SGC"
CarpetaZip=r"D:\SGC\EPIS"
NombreZip="POZOS_EPIS_SGC"

arcpy.env.overwriteOutput=True

today = datetime.date.today()
Nombre=str(today).replace("-","_")

wellsShapeFile=CarpetaZip+ os.sep+ NombreZip+"_"+Nombre+".shp"
arcpy.FeatureClassToFeatureClass_conversion(FeatureClass,CarpetaZip, NombreZip+"_"+Nombre+".shp","","UWI \"UWI\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,UWI,-1,-1;"
                                                                                    "WELL_NAME \"Nombre Pozo\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_NAME,-1,-1;"
                                                                                    "WELL_COUNT \"Pais\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_COUNT,-1,-1;"
                                                                                    "DEPARTAMEN \"Departamento\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,DEPARTAMEN,-1,-1;"
                                                                                    "WELL_COU_1 \"Municipio\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_COU_1,-1,-1;"
                                                                                    "WELL_TVD \"TVD\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_TVD,-1,-1;"
                                                                                    "WELL_KB_EL \"KB_ELEVACION\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_KB_EL,-1,-1;"
                                                                                    "ROTARY_ELE \"MESA_ROTATORIA_ELEVACION\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,ROTARY_ELE,-1,-1;"
                                                                                    "WELL_DRILL \"MD\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_DRILL,-1,-1;"
                                                                                    "WELL_GROUN \"ELEVACION_TERRENO\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_GROUN,-1,-1;"
                                                                                    "FIELD_ABRE \"Campo\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,FIELD_ABRE,-1,-1;"
                                                                                    "GEOLOGIC_P \"Unidad Geológica\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,GEOLOGIC_P,-1,-1;"
                                                                                    "CONTRATO \"Contrato\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,CONTRATO,-1,-1;"
                                                                                    "WELL_LONGI \"LONGITUD_WGS84\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_LONGI,-1,-1;"
                                                                                    "WELL_LATIT \"LATITUD_WGS84\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_LATIT,-1,-1;"
                                                                                    "WELL_X_COO \"X_TORRE_DOC\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_X_COO,-1,-1;"
                                                                                    "WELL_Y_COO \"Y_TORRE_DOC\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_Y_COO,-1,-1;"
                                                                                    "WELL_X_DEP \"X_FONDO_DOC\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_X_DEP,-1,-1;"
                                                                                    "WELL_Y_DEP \"Y_FONDO_DOC\" true true false 8 Double 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_Y_DEP,-1,-1;"
                                                                                    "DATUM \"Datum\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,DATUM,-1,-1;"
                                                                                    "WELL_SPUD_ \"INICIO_PERFORACION\" true true false 8 Date 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_SPUD_,-1,-1;"
                                                                                    "COORD_QUAL \"coord_qual\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,COORD_QUAL,-1,-1;"
                                                                                    "DOCUMENTO \"Documento\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,DOCUMENTO,-1,-1;"
                                                                                    "COMMENT_ \"COMENTARIOS\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,COMMENT_,-1,-1;"
                                                                                    "WELL_COMPL \"TERMINACION_POZO\" true true false 8 Date 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_COMPL,-1,-1;"
                                                                                    "WELL_CLA_1 \"CLAS_LAHEE_F4CR\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_CLA_1,-1,-1;"
                                                                                    "WELL_STA_1 \"CLAS_LAHEE_F6CR\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELL_STA_1,-1,-1;"
                                                                                    "WELLTYPE \"TIPO_DESVIACION\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,WELLTYPE,-1,-1;"
                                                                                    "FECHA_ACTU \"Fecha Actualización\" true true false 8 Date 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,FECHA_ACTU,-1,-1;"
                                                                                    "INSERTED_B \"inserted_b\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,INSERTED_B,-1,-1;"
                                                                                    "ENTITLEMEN \"entitlemen\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,ENTITLEMEN,-1,-1;"
                                                                                    "ACTUALIZAD \"Actualizado\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,ACTUALIZAD,-1,-1;"
                                                                                    "CREAT_DATE \"Fecha Creación\" true true false 8 Date 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,CREAT_DATE,-1,-1;"
                                                                                    "OPERATOR_W \"Operador\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,OPERATOR_W,-1,-1;"
                                                                                    "COMPANY_CO \"Compañia\" true true false 254 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,COMPANY_CO,-1,-1;"
                                                                                    "CARGA_SGC \"Cargar SGC\" true true false 10 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,CARGA_SGC,-1,-1;"
                                                                                    "CONT_EPIS \"Contrato EPIS\" true true false 150 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,CONT_EPIS,-1,-1;"
                                                                                    "RELACIONAD \"Relacionado\" true true false 2 Short 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,RELACIONADO,-1,-1;"
                                                                                    "CLAS_FINAL \"CLAS_FINAL_F6CR\" true true false 100 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,CLAS_FINAL_F6CR,-1,-1;"
                                                                                    "FORMACION_ \"FORMACION_OBJETIVO_F4CR\" true true false 100 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,FORMACION_OBJETIVO_F4CR,-1,-1;"
                                                                                    "FORMACION1 \"FORMACION_F6CR\" true true false 100 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,FORMACION_F6CR,-1,-1;"
                                                                                    "ESTRUCTURA \"ESTRUCTURA_F6CR\" true true false 100 Text 0 0 ,First,#,D:\\SGC\\EPIS\\epis_17_11.mdb\\EPIS\\POZOS_EPIS_SGC,ESTRUCTURA_F6CR,-1,-1;"
                                                                                    "WELL_Y_DEP \"Y_FONDO_DOC\" true true false 50 Text 0 0 ,First,#", "")

wellsZipFile = CarpetaZip+os.sep+NombreZip+".zip"

def zipShapefile(inShapefile, newZipFN):
    print 'Comprimiendo '+inShapefile+' to '+newZipFN

    if not (os.path.exists(inShapefile)):
       print inShapefile + ' Does Not Exist'
       return False

    if (os.path.exists(newZipFN)):
       print 'Borrando '+newZipFN
       os.remove(newZipFN)

    if (os.path.exists(newZipFN)):
       print 'No se puede borrar'+newZipFN
       return False

    zipobj = zipfile.ZipFile(newZipFN,'w')

    for infile in glob.glob( inShapefile.lower().replace(".shp",".*")):
       print infile
       zipobj.write(infile,os.path.basename(infile),zipfile.ZIP_DEFLATED)

    zipobj.close()
    return True

zipShapefile(wellsShapeFile,wellsZipFile)
try:
    arcpy.Delete_management(wellsShapeFile)
except:
    arcpy.AddMessage("no se puede borrar el shape")
print "Terminado!"
