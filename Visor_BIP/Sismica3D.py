import zipfile
import sys
import os
import glob
import datetime

import arcpy
FeatureClass=r"E:\Scripts\Visor_BIP\EPIS_ODA_PROD.sde\EPIS.EPIS\EPIS.SISMICA3D_EPIS_SGC"
CarpetaZip=r"E:\Archivos_Geoportal\EPIS"
NombreZip="SISMICA3D_EPIS_SGC"

arcpy.env.overwriteOutput=True

today = datetime.date.today()
Nombre=str(today).replace("-","_")

wellsShapeFile=CarpetaZip+ os.sep+ NombreZip+"_"+Nombre+".shp"
arcpy.FeatureClassToFeatureClass_conversion(FeatureClass,CarpetaZip, NombreZip+"_"+Nombre+".shp")

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
