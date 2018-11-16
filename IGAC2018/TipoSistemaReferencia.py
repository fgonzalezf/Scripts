import arcpy, os,sys

capa=r"C:\Users\Desarrollo\Downloads\MagnaPro4\data\shp\Magna\planchas\Central.shp"
arcpy.env.workspace=capa
sptref=arcpy.Describe(capa)
stref=sptref.spatialReference
arcpy.env.outputCoordinateSystem= stref

if stref.PCSCode==0:
    print "Sistema de referencia Geografico"
else:
    print "Sistema de referencia Plano"
