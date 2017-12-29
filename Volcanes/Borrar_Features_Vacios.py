import arcpy, os,sys

Geodatabase= r"D:\Visor_Volacnes\GDB_Volcanes\Mapa_Amenaza_Volcanica_VPA_2DA_Version.gdb"

arcpy.env.workspace=Geodatabase

ListaDatasets=arcpy.ListDatasets()

for dataset in ListaDatasets:
    DatasetIn = Geodatabase+ os.sep+ dataset
    arcpy.env.workspace =DatasetIn
    ListaFeat= arcpy.ListFeatureClasses()
    for fc in ListaFeat:
        fcIn = Geodatabase+ os.sep+ dataset+os.sep+fc
        count = int(arcpy.GetCount_management(fcIn).getOutput(0))
        if count==0:
            print fc + "..."
            arcpy.Delete_management(fcIn)