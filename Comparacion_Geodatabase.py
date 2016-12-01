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
#ShapefileCorte=sys.argv[3]
#Query=sys.argv[4]
#BufferSeleccion= sys.argv[6]
Salida1=""
Salida2=""
arcpy.env.overwriteOutput=True

if GeodatabaseEntrada.find(".gdb")==-1:
    Xml=GeodatabaseEntrada.replace(".mdb","_.xml")
    Fileprj = open (GeodatabaseSalida[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+".txt", "w")
    Fileprj.write("ERRORES: " + "\n")
    typeEnt=False
else:
    Xml=GeodatabaseEntrada.replace(".gdb",".xml")
    Fileprj = open (GeodatabaseSalida[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+".txt", "w")
    Fileprj.write("ERRORES: " + "\n")
    typeEnt=True

if GeodatabaseSalida.find(".gdb")==-1:
    try:

        arcpy.CreatePersonalGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"ENTRADA_SALIDA")
        #arcpy.CreatePersonalGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"SALIDA_ENTRADA")
        Salida1=os.path.join(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"ENTRADA_SALIDA")+".mdb"
        Salida2=os.path.join(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"SALIDA_ENTRADA")+".mdb"
    except Exception as ex:
        arcpy.AddMessage("Error Creando Geodatabase..." +ex.message)
    typeSal=False
else:
    arcpy.CreateFileGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"ENTRADA_SALIDA")
    #arcpy.CreateFileGDB_management(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"SALIDA_ENTRADA")
    Salida1=os.path.join(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"ENTRADA_SALIDA")+".gdb"
    Salida2=os.path.join(os.path.dirname(GeodatabaseSalida),os.path.basename(GeodatabaseSalida)[:-4]+"_"+os.path.basename(GeodatabaseEntrada)[:-4]+"SALIDA_ENTRADA")+".gdb"
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

arcpy.AddMessage("Exportando Esquema...")
exportar(GeodatabaseEntrada,Xml,typeEnt)
arcpy.AddMessage("Importando Esquema...")
importar(Salida1,Xml,typeSal)
arcpy.Copy_management(Salida1,Salida2)
#importar(Salida2,Xml,typeSal)
os.remove(Xml)


arcpy.AddMessage("Cortando Geodatabase")
arcpy.env.workspace = GeodatabaseEntrada
datasetList = arcpy.ListDatasets()
for dataset in datasetList:
    arcpy.env.workspace = GeodatabaseEntrada + "/" + dataset
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
            result = int(arcpy.GetCount_management(fc).getOutput(0))
            fcSal=GeodatabaseSalida + "/" + dataset + "/" + fc
            fcSal1=Salida1+ "/" + dataset + "/" + fc
            fcSal2=Salida2+ "/" + dataset + "/" + fc
            try:
                if result>0:
                    arcpy.AddMessage(fc)
                    desc = arcpy.Describe(fc)
                    if(desc.featureType!="Annotation"):
                        arcpy.Erase_analysis(fc,fcSal,"in_memory/Salida1")
                        arcpy.Append_management("in_memory/Salida1",fcSal1,"NO_TEST")
                        arcpy.Erase_analysis(fcSal,fc,"in_memory/Salida2")
                        arcpy.Append_management("in_memory/Salida2",fcSal2,"NO_TEST")
                        arcpy.Delete_management("in_memory/Salida1")
                        arcpy.Delete_management("in_memory/Salida2")
            except Exception as ex:
                arcpy.AddMessage("Error..."+ex.message)
                Fileprj.write("Error Seleccionando: "+ fc + "\n")
Fileprj.close()
del datasetList
del fcList
