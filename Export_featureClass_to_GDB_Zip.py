import zipfile
import sys
import os
import glob

import arcpy
FeatureClass=sys.argv[1]
CarpetaZip=sys.argv[2]

arcpy.CreatePersonalGDB_management(CarpetaZip,os.path.basename(FeatureClass)+".mdb","9.1")

GDB=CarpetaZip+os.sep+os.path.basename(FeatureClass)+".mdb"

wellsShapeFile=GDB
arcpy.FeatureClassToFeatureClass_conversion(FeatureClass,GDB,os.path.basename(FeatureClass))

wellsZipFile = wellsShapeFile[:-4]+".zip"

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
print "Terminado!"

