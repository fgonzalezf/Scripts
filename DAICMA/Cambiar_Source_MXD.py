import arcpy, os,sys

CarpetaEntrada=r"C:\Users\APN\Documents\APN\Migracion_Server\Zonas"
CarpetaSalida=r"C:\Users\APN\Documents\APN\Migracion_Server\Zonas2"
arcpy.env.workspace=CarpetaEntrada

pathin=r"C:\Users\maicolvelasquez\AppData\Roaming\Esri\Desktop10.2\ArcCatalog\SDE_VISORES.sde"
pathOut=r"C:\Users\APN\Documents\APN\Migracion_Server\Scripts\GDB\Bk_GDB.gdb"

ListaCarpetas=arcpy.ListWorkspaces("*", "Folder")

for folder in ListaCarpetas:
    print folder
    arcpy.CreateFolder_management(CarpetaSalida,os.path.basename(folder))
    arcpy.env.workspace = folder
    ListaMxd = arcpy.ListFiles("*.mxd")
    for mxdfile in ListaMxd:
        print mxdfile
        mxd = arcpy.mapping.MapDocument(folder+ os.sep+ mxdfile)
        mxd.findAndReplaceWorkspacePaths(pathin, pathOut)
        mxd.saveACopy(CarpetaSalida+ os.sep +os.path.basename(folder)+ os.sep+ mxdfile,"10.1")
        del mxd