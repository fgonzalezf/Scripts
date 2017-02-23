import zipfile
import sys
import os
import glob

import arcpy
FeatureClass=sys.argv[1]
CarpetaZip=sys.argv[2]

wellsShapeFile=CarpetaZip+ os.sep+ os.path.basename(FeatureClass)+".shp"
arcpy.FeatureClassToFeatureClass_conversion(FeatureClass,CarpetaZip,os.path.basename(FeatureClass)+".shp")

wellsZipFile = wellsShapeFile[:-4]+"Zip"+".zip"

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