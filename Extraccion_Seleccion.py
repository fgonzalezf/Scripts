import arcpy,sys,os,arcgisscripting
import comtypes
from comtypes.client import GetModule
from comtypes.client import CreateObject
#GeodatabaseEntrada=r"X:\PRUEBAS\Seleccion\BLOQUE6.gdb"
#GeodatabaseSalida=r"X:\PRUEBAS\Seleccion\327IIIA_6.mdb"
#ShapefileCorte=r"X:\PRUEBAS\Seleccion\327IIIA.shp"
#LinkAnnotation="true"
#Query="327IIIA"
#BufferSeleccion= sys.argv[6]

GeodatabaseEntrada=sys.argv[1]
GeodatabaseSalida=sys.argv[2]
ShapefileCorte=sys.argv[3]
Query=sys.argv[4]
#BufferSeleccion= sys.argv[6]

arcpy.env.overwriteOutput=True

if GeodatabaseEntrada.find(".gdb")==-1:
    Xml=GeodatabaseEntrada.replace(".mdb","_.xml")
    Fileprj = open (GeodatabaseSalida[:-4]+".txt", "w")
    Fileprj.write("ERRORES: " + "\n")
    typeEnt=False
else:
    Xml=GeodatabaseEntrada.replace(".gdb",".xml")
    Fileprj = open (GeodatabaseSalida[:-4]+".txt", "w")
    Fileprj.write("ERRORES: " + "\n")
    typeEnt=True

if GeodatabaseSalida.find(".gdb")==-1:
    try:
        arcpy.CreatePersonalGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida))
    except Exception as ex:
        arcpy.AddMessage("Error Creando Geodatabase..." +ex.message)
    typeSal=False
else:
    arcpy.CreateFileGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida))
    typeSal=True
    
def NewObj(MyClass, MyInterface):   
    try:
        ptr=CreateObject(MyClass, interface=MyInterface)
        return ptr
    except:
        return None
def CType(obj, interface):
    try:
        newobj = obj.QueryInterface(interface)
        return newobj
    except:
        return None 
def CLSID(MyClass):
    return str(MyClass._reg_clsid_)

def arrayCamposFeat(FeatuareClass):
    listaCampos=arcpy.ListFields(FeatuareClass)
    listaNombres=[]
    for field in listaCampos:
        if field.name.upper()==u'SHAPE'.upper():
            listaNombres.append("SHAPE@")
        elif field.name.upper()=='OBJECTID'.upper():
            listaNombres.append(u"OID@")
        elif  field.name.upper()=='SHAPE_Length'.upper() or field.name.upper()=='SHAPE_Area'.upper() or field.name.upper()=='OVERRIDE'.upper():
            pass
        else:
            listaNombres.append(field.name.upper())
    return listaNombres

def arrayCamposAnot(FeatuareClass):
    listaCampos=arcpy.ListFields(FeatuareClass)
    listaNombres=[]
    for field in listaCampos:
        if field.name.upper()==u'SHAPE'.upper():
            listaNombres.append("SHAPE@")
        elif field.name.upper()=='OBJECTID'.upper():
            listaNombres.append(u"OID@")
        elif  field.name.upper()=='SHAPE_Length'.upper() or field.name.upper()=='SHAPE_Area'.upper():
            pass
        else:
            listaNombres.append(field.name.upper())
    return listaNombres

def appendOutTestFeat(FeatIn, FeatOut,workspace):
    OBIDS={}
    CamposIn= arrayCamposFeat(FeatIn)
    CamposOut= arrayCamposFeat(FeatOut)
    camposIguales=[]
    for camposEnt in CamposIn:
        for camposSal in CamposOut:
            if camposEnt==camposSal:
                camposIguales.append(camposEnt)
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(True, False)
    edit.startOperation()
    cursor2 = arcpy.da.InsertCursor(FeatOut,camposIguales)
    with arcpy.da.SearchCursor(FeatIn,camposIguales) as cursor:
        for row in cursor:
            IdNuevo=cursor2.insertRow(row)
            OBIDS[int(row[0])]=int(IdNuevo)
    edit.stopOperation()
    edit.stopEditing(True)
    del cursor2
    del row
    return OBIDS

def appendOutTestAnot(FeatIn, FeatOut, workspace,Diccionario):
    CamposIn= arrayCamposAnot(FeatIn)
    CamposOut= arrayCamposAnot(FeatOut)
    print CamposIn
    print CamposOut
    #igualacion de campos
    camposIguales=[]
    for camposEnt in CamposIn:
        for camposSal in CamposOut:
            if camposEnt==camposSal:
                camposIguales.append(camposEnt)
    print camposIguales
    #with arcpy.da.Editor(workspace) as edit:
        #print edit.isEditing
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(True, False)
    edit.startOperation()
    cursor2 = arcpy.da.InsertCursor(FeatOut,camposIguales)
    with arcpy.da.SearchCursor(FeatIn,camposIguales) as cursor:
            for row in cursor:
                #rwint=int(row[0])
                #arcpy.AddMessage(str(int(row[0])))
                #row[0]=Diccionario[rwint]
                cursor2.insertRow(row)
    edit.stopOperation()
    edit.stopEditing(True)
    del cursor2
    del row



def exportar (db, xmlFile,type):
    esriGeodatabase= GetModule(r"C:\ArcGIS\Desktop10.3\com\esriGeoDatabase.olb")
    esriSystem=GetModule(r"C:\ArcGIS\Desktop10.3\com\esriSystem.olb")
    esriGeoadatabaseDistributed=GetModule(r"C:\ArcGIS\Desktop10.3\com\esriGeoDatabaseDistributed.olb")
    esriDataSourcesGDB=GetModule(r"C:\ArcGIS\Desktop10.3\com\esriDataSourcesGDB.olb")
    if (type== True):
        pWSF= NewObj(esriDataSourcesGDB.FileGDBWorkspaceFactory,esriGeodatabase.IWorkspaceFactory)
    else:
        pWSF= NewObj(esriDataSourcesGDB.AccessWorkspaceFactory,esriGeodatabase.IWorkspaceFactory)
    pWS= pWSF.OpenFromFile(db, 0)
    pGDBExporter=NewObj(esriGeoadatabaseDistributed.GdbExporter,esriGeoadatabaseDistributed.IGdbXmlExport)
    pGDBExporter.ExportWorkspaceSchema(pWS, xmlFile, False, False)

def importar (db, xmlFile,type):
    esriGeodatabase= GetModule(r"C:\ArcGIS\Desktop10.3\com\esriGeoDatabase.olb")
    esriSystem=GetModule(r"C:\ArcGIS\Desktop10.3\com\esriSystem.olb")
    esriGeoadatabaseDistributed=GetModule(r"C:\ArcGIS\Desktop10.3\com\esriGeoDatabaseDistributed.olb")
    esriDataSourcesGDB=GetModule(r"C:\ArcGIS\Desktop10.3\com\esriDataSourcesGDB.olb")
    if (type== True):
        pWSF= NewObj(esriDataSourcesGDB.FileGDBWorkspaceFactory,esriGeodatabase.IWorkspaceFactory)
    else:
        pWSF= NewObj(esriDataSourcesGDB.AccessWorkspaceFactory,esriGeodatabase.IWorkspaceFactory)
    pWS= pWSF.OpenFromFile(db, 0) 
    pEnumName =  esriGeodatabase.IEnumNameMapping
    pImporter=NewObj(esriGeoadatabaseDistributed.GdbImporter,esriGeoadatabaseDistributed.IGdbXmlImport)
    pEnumName=pImporter.GenerateNameMapping(xmlFile,pWS)
    pImporter.ImportWorkspace(xmlFile , pEnumName[0] , pWS , True )
    
def AutoCreateAnnot (FeatRuta):
    esriGeodatabase= GetModule(r"C:\ArcGIS\Desktop10.3\com\esriGeoDatabase.olb")
    esriGeoprocessing= GetModule(r"C:\ArcGIS\Desktop10.3\com\esriGeoprocessing.olb")
    esriCarto= GetModule(r"C:\ArcGIS\Desktop10.3\com\esriCarto.olb")
    
    pGputility= NewObj(esriGeoprocessing.GPUtilities,esriGeoprocessing.IGPUtilities)
    pFeatureClass=esriGeodatabase.IFeatureClass
    pAnnoClass=esriCarto.IAnnoClass
    pAnnoClassAdmin=esriCarto.IAnnoClassAdmin
    try:
        pFeatureClass = pGputility.OpenFeatureClassFromString(FeatRuta)
        pAnnoClass =CType(pFeatureClass.Extension, pAnnoClass)
        pAnnoClassAdmin = CType(pAnnoClass, pAnnoClassAdmin)
    except Exception as ex:
        arcpy.AddMessage("Error en Apagado Anotaciones..." + ex.message)
    
    pAnnoClassAdmin.AutoCreate = False
    pAnnoClassAdmin.UpdateProperties()

def Mapa(fieldmappings,FeatEntrada, CampoEntrada , CampoSalida):
        fieldmap = fieldmappings.getFieldMap(fieldmappings.findFieldMapIndex(CampoSalida))
        fieldmap.addInputField(FeatEntrada, CampoEntrada)
        fieldmappings.replaceFieldMap(fieldmappings.findFieldMapIndex(CampoSalida), fieldmap)
        #fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(CampoEntrada))
        return fieldmappings

def seleccionAnot(Entrada,FeatSelect,Salida,Diccionario):

    layer1=arcpy.MakeFeatureLayer_management(Entrada, "Entrada_lyr")
    layer2=arcpy.SelectLayerByLocation_management ("Entrada_lyr", "INTERSECT",FeatSelect,"-1 Centimeters","NEW_SELECTION")

    AutoCreateAnnot(Salida)
    appendOutTestAnot("Entrada_lyr",Salida,GeodatabaseSalida,Diccionario)
    del layer1
    del layer2

def seleccionFeat(Entrada,FeatSelect,Salida):

    layer1=arcpy.MakeFeatureLayer_management(Entrada, "Entrada_lyr")
    layer2=arcpy.SelectLayerByLocation_management ("Entrada_lyr", "INTERSECT",FeatSelect,"-1 Centimeters","NEW_SELECTION")

    Diccionario=appendOutTestFeat("Entrada_lyr",Salida,GeodatabaseSalida)

    del layer1
    del layer2
    return Diccionario



arcpy.AddMessage("Exportando Esquema...")  
exportar(GeodatabaseEntrada,Xml,typeEnt)
arcpy.AddMessage("Importando Esquema...")  
importar(GeodatabaseSalida,Xml,typeSal)
os.remove(Xml)

###################
#CORTE = arcpy.FeatureClassToFeatureClass_conversion(ShapefileCorte,GeodatabaseEntrada + "/Indice_Mapas","CORTE" )
CORTE= arcpy.MakeFeatureLayer_management(ShapefileCorte,"CORTE")
arcpy.AddMessage("Cortando Geodatabase")
arcpy.env.workspace = GeodatabaseEntrada
datasetList = arcpy.ListDatasets()
for dataset in datasetList:
    arcpy.env.workspace = GeodatabaseEntrada + "/" + dataset
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
        if fc != "CORTE":
            result = int(arcpy.GetCount_management(fc).getOutput(0))

            try:
                if result>0:
                    arcpy.AddMessage(fc)
                    fcSal=GeodatabaseSalida + "/" + dataset + "/" + fc
                    desc = arcpy.Describe(fc)

                    if(desc.featureType!="Annotation"):
                        Diccionario = seleccionFeat(GeodatabaseEntrada+os.sep+dataset+os.sep+fc,CORTE,fcSal)
                        if(arcpy.Exists(fc+"_Anot")):
                            seleccionAnot(GeodatabaseEntrada+os.sep+dataset+os.sep+fc+"_Anot", CORTE , fcSal+"_Anot",Diccionario)

            except Exception as ex:
                arcpy.AddMessage("Error..."+ex.message)
                Fileprj.write("Error Seleccionando: "+ fc + "\n")
del datasetList
del fcList

if Query != "":
    try:
        arcpy.env.workspace = GeodatabaseEntrada
        tablas = arcpy.ListTables()
        for tabla in tablas:
            arcpy.AddMessage( "Cargando Tabla..."+ tabla)
            tbSal= GeodatabaseSalida+ os.sep+tabla
            plancha = arcpy.AddFieldDelimiters(tabla, "PLANCHA")
            sqlQuery= plancha+"="+"'"+Query+"'"
            arcpy.AddMessage( "ExSql..."+sqlQuery)
            tab=arcpy.MakeTableView_management(tabla, "tabla_query", plancha+"="+"'"+Query+"'")
            arcpy.Append_management("tabla_query",tbSal,"NO_TEST")
            arcpy.Delete_management("tabla_query")
    except Exception as ex:
        if tab:
            del tab
        arcpy.AddMessage("Error Cargando tablas Metadatos.."+ ex.message)  
        Fileprj.write("Error Cargando: "+ tabla + "\n") 
            
del CORTE
Fileprj.close()












