__author__ = 'fernando.gonzalez'
import arcpy, os, sys
from comtypes.client import CreateObject
from comtypes.client import GetModule

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

def SetAutoCreateAnnot (FeatRuta, InVal = False):
        esriGeodatabase= GetModule(r"c:\Program Files (x86)\ArcGIS\Desktop10.0\com\esriGeoDatabase.olb")
        esriGeoprocessing= GetModule(r"c:\Program Files (x86)\ArcGIS\Desktop10.0\com\esriGeoprocessing.olb")
        esriCarto= GetModule(r"c:\Program Files (x86)\ArcGIS\Desktop10.0\com\esriCarto.olb")

        pGputility= NewObj(esriGeoprocessing.GPUtilities,esriGeoprocessing.IGPUtilities)
        pFeatureClass=esriGeodatabase.IFeatureClass
        pAnnoClass=esriCarto.IAnnoClass
        pAnnoClassAdmin=esriCarto.IAnnoClassAdmin
        try:
            pFeatureClass = pGputility.OpenFeatureClassFromString(FeatRuta)
            pAnnoClass =CType(pFeatureClass.Extension, pAnnoClass)
            pAnnoClassAdmin = CType(pAnnoClass, pAnnoClassAdmin)
        except:
            arcpy.AddError("Error en apagado")
            raise

        pAnnoClassAdmin.AutoCreate = InVal
        pAnnoClassAdmin.UpdateProperties()

def GetListDSetnFC(inGeoDB):
    arcpy.AddMessage("Listando los datasets y featureclasses de la Geodatabase %s" %inGeoDB)
    arcpy.env.workspace = inGeoDB
    try:
        DictFC = {}
        for CurDset in arcpy.ListDatasets():
            DictFC [CurDset] = arcpy.ListFeatureClasses("*","",CurDset)
        DictFC [''] = arcpy.ListFeatureClasses()
        DictFC [''] += arcpy.ListTables()
    except:
        arcpy.AddError('    Error recorriendo los elementos de la geodatabase. Error %s' %arcpy.GetMessages(2))
    finally:
        return DictFC

entrada=r'X:\PRUEBAS\Sandra_Gamba\Pruebas\386ID.mdb'
salida=r'X:\PRUEBAS\Sandra_Gamba\Pruebas\386IIC.mdb'

DictFeat= GetListDSetnFC(entrada)

for dataset in sorted(DictFeat.keys()):
    for Feat in sorted(DictFeat[dataset]):
        NumeroElementos = int(arcpy.GetCount_management(Feat).getOutput(0))
        if NumeroElementos > 0:
            print "    FEATURE CLASS %s (DATASET %s)" %(Feat, dataset)


#rows= arcpy.SearchCursor(entrada)
#rows2=arcpy.InsertCursor(salida)

#for row in rows:
    #rows2.insertRow(row)

#del row
#del rows
#del rows2