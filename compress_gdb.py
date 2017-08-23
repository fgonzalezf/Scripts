import arcpy
RutaConexion=r'Database Connections/SDE.sde'
conexiones=[r'Database Connections/SDE.sde']
LogReconciliacion=r"C:/Temp"

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
arcpy.AcceptConnections(RutaConexion, True)

for simma in conexiones:
    try:
        userName = arcpy.Describe(simma).connectionProperties.user.lower()
        dataList = arcpy.ListTables( userName + '.') + arcpy.ListFeatureClasses(userName + '.') + arcpy.ListRasters(userName + '.')
        #userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

        for dataset in arcpy.ListDatasets():
            dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
            print arcpy.ListFeatureClasses(feature_dataset=dataset)
        print "Indexando"
        arcpy.RebuildIndexes_management(simma, "NO_SYSTEM", dataList, "ALL")
        print "Analizando"
        arcpy.AnalyzeDatasets_management(simma, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    except Exception as ex:
        print "Error en "+simma+" "+ex.message

print "Aceptando conexiones"
arcpy.AcceptConnections(RutaConexion, True)