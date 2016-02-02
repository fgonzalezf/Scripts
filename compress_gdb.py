import arcpy
RutaConexion='Database Connections/SDE_PRUB.sde'
LogReconciliacion=r"c:/temp/reconcilelog.txt"

arcpy.env.workspace = RutaConexion
workspace = arcpy.env.workspace
userList = arcpy.ListUsers(RutaConexion)
for user in userList:
    print user
print "Cerrando Conexiones"
arcpy.AcceptConnections(RutaConexion, False)
print "Desconectando Usuarios"
arcpy.DisconnectUser(RutaConexion, "ALL")
versionList = arcpy.ListVersions(RutaConexion)
for version in versionList:
    print version
print "Reconciliando"
arcpy.ReconcileVersions_management(RutaConexion, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION",LogReconciliacion)
print "Realizando Compress"
arcpy.Compress_management(RutaConexion)
print "Aceptando conexiones"
arcpy.AcceptConnections(RutaConexion, True)

dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

for dataset in arcpy.ListDatasets():
    dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
    print arcpy.ListFeatureClasses(feature_dataset=dataset)
print "Indexando"
#arcpy.RebuildIndexes_management(workspace, "SYSTEM", dataList, "ALL")
print "Analizando"
arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
