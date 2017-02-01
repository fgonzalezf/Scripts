import arcpy, os,sys

mxd = arcpy.mapping.MapDocument(r"D:\Pruebas\Corte_geodatabase\PRUEBA\Workspace.mxd")

# Busqueda del workspace del primer layer del dataframe activo
# si todos los workspace del mxd no son iguales solo se cambiara el primero encontrado
df = mxd.activeDataFrame
lyr = arcpy.mapping.ListLayers(mxd,"*",df)[0]
worspaceEntrada= lyr.workspacePath
worspaceSalida=r"D:\Pruebas\Corte_geodatabase\PRUEBA\141IVC.mdb"

mxd.findAndReplaceWorkspacePaths(worspaceEntrada,worspaceSalida)

#salvando una copia del Mxd con los workspacepath modificados

mxd.saveACopy(r"D:\Pruebas\Corte_geodatabase\PRUEBA\Workspace3.mxd")
del mxd
