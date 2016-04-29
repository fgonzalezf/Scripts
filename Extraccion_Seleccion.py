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
LinkAnnotation=sys.argv[4]
Query=sys.argv[5]
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

def seleccion(Entrada,FeatSelect,Salida,workspace):

    layer1=arcpy.MakeFeatureLayer_management(Entrada, "Entrada_lyr")
    layer2=arcpy.SelectLayerByLocation_management ("Entrada_lyr", "INTERSECT",FeatSelect,"-1 Centimeters","NEW_SELECTION")

    AutoCreateAnnot(Salida)
    arcpy.Append_management("Entrada_lyr",Salida,"TEST")
    del layer1
    del layer2

def seleccionCalc(Entrada,FeatSelect,Salida,workspace,FielMapping):

    layer1=arcpy.MakeFeatureLayer_management(Entrada, "Entrada_lyr")
    layer2=arcpy.SelectLayerByLocation_management ("Entrada_lyr", "INTERSECT",FeatSelect,"-1 Centimeters","NEW_SELECTION")

    fieldmp=Mapa(FielMapping,"Entrada_lyr","OBJECTID","TempId")
    arcpy.Append_management("Entrada_lyr",Salida,"NO_TEST",fieldmp)

    del layer1
    del layer2
def seleccionFeat(Entrada,FeatSelect,Salida,workspace):

    layer1=arcpy.MakeFeatureLayer_management(Entrada, "Entrada_lyr")
    layer2=arcpy.SelectLayerByLocation_management ("Entrada_lyr", "INTERSECT",FeatSelect,"-1 Centimeters","NEW_SELECTION")

    arcpy.Append_management("Entrada_lyr",Salida,"NO_TEST")

    del layer1
    del layer2



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
                        if(arcpy.Exists(fc+"_Anot")):
                            seleccion(GeodatabaseEntrada+os.sep+dataset+os.sep+fc+"_Anot", CORTE , fcSal+"_Anot",GeodatabaseEntrada + "/" + dataset)
                        if (LinkAnnotation=="true"):
                            try:
                                arcpy.AddField_management(fcSal,"TempId","LONG")
                            except:
                                arcpy.AddMessage("Campo ya creado")
                        if (LinkAnnotation=="true"):
                            fieldmapping = arcpy.FieldMappings()
                            fieldmapping.addTable(fc)
                            fieldmapping.addTable(fcSal)
                            seleccionCalc(GeodatabaseEntrada+os.sep+dataset+os.sep+fc, CORTE , fcSal,GeodatabaseEntrada + "/" + dataset,fieldmapping)
                        else:
                            seleccionFeat(GeodatabaseEntrada+os.sep+dataset+os.sep+fc, CORTE , fcSal,GeodatabaseEntrada + "/" + dataset)

            except Exception as ex:
                arcpy.AddMessage("Error..."+ex.message)
                Fileprj.write("Error Cortando: "+ fc + "\n")                               
del datasetList
del fcList

if (LinkAnnotation=="true"): 
    arcpy.AddMessage("Relacionando Anotaciones")
    arcpy.Delete_management(CORTE)
    arcpy.env.workspace = GeodatabaseSalida
    datasetList = arcpy.ListDatasets()
    for dataset in datasetList:
        arcpy.env.workspace = GeodatabaseSalida + "/" + dataset
        fcList = arcpy.ListFeatureClasses()
        for fc in fcList:
            try:    
                desc = arcpy.Describe(fc)
                result = int(arcpy.GetCount_management(fc).getOutput(0))
                if(result>0):
                    if(desc.featureType=="Annotation"):                  
                        Annotacion=fc
                        Feature=GeodatabaseSalida + "/" + dataset+"/"+fc.replace("_Anot","")
                        arcpy.AddMessage("Relacionado: " + fc + " Con " + fc.replace("_Anot",""))
                        layer=arcpy.MakeFeatureLayer_management(fc)
                        layer2=arcpy.MakeFeatureLayer_management(Feature)                    
                        arcpy.AddJoin_management(layer,"FeatureID",layer2,"TempId")
                        arcpy.CalculateField_management(layer, fc+".FeatureID","["+fc.replace("_Anot","")+".OBJECTID]","VB")                          
                        del layer
                        del layer2
            except Exception as ex:
                arcpy.AddMessage("Error Relacionado Campos.."+ ex.message)               
    del datasetList
    del fcList
    arcpy.AddMessage("Borrando Campos Temporales")
    arcpy.env.workspace = GeodatabaseEntrada
    datasetList = arcpy.ListDatasets()
    for dataset in datasetList:
        arcpy.env.workspace = GeodatabaseEntrada + "/" + dataset
        fcList = arcpy.ListFeatureClasses()
        for fc in fcList:
            try:
                desc = arcpy.Describe(fc)
                result = int(arcpy.GetCount_management(fc).getOutput(0))
                if result>0: 
                    if(desc.featureType!="Annotation"):
                        arcpy.AddMessage(fc)
                        fcSal=GeodatabaseSalida + "/" + dataset + "/" + fc
                        arcpy.DeleteField_management(fc,"TempId")
                        arcpy.DeleteField_management(fcSal,"TempId")
            except Exception as ex:
                arcpy.AddMessage("Error Borrando Campos Temporales..."+ ex.message) 
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












