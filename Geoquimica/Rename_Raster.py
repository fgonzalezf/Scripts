import arcpy

Geodatabase = r"D:\Geoquimica\2018\Nativos\Tematico\Atlas_Geoquimico_2017.gdb"

arcpy.env.workspace= Geodatabase

ListRasters = arcpy.ListRasters()

for raster in ListRasters:
    arcpy.Rename_management(raster,raster.split("_")[0]+"_2018")
    print raster.split("_")[0]+"_2018"