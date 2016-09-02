'''
Created on 23/07/2014
@author: cmorenob
Funcionalidad: Migrar multiples geodatabases personales a una Geodatabase (preferiblemente de archivo debido a la flexibilidad en el tamanio)
Observaciones:
    1. Requiere que la GeoDB de salida tenga la estructura creada
    2. La GeoDB de salida debe contar con la estructura vigente con anotaciones
    3. Requiere que las Geodatabases involucradas no esten siendo usadas 
    4. El script no cuenta con tildes debido a los errores que estas generan en su ejecucion 
Palabras clave: append, migrate, migracion, annotation, anotacion, personal geodatabase, file geodatabase
Detalle version: esta version contiene un modo de actualizar rutas puntual y no masivo para evitar interrupciones en procesos de calculo. Ademas se realizan tareas de division de procesos

#################################################################################################
#####################################################################################################
############################

'''
import os, arcpy, time,sys
from comtypes.client import CreateObject
from comtypes.client import GetModule

reload(sys)
sys.setdefaultencoding("utf-8")
InGeoDBs = arcpy.GetParameterAsText(0)
InOutGeoDB = arcpy.GetParameterAsText(1)
InAutoCreateAnnot = arcpy.GetParameterAsText(2) 

if InAutoCreateAnnot.lower() == 'true':
    InAutoCreateAnnot = True
else:
    InAutoCreateAnnot = False

SufixAnnotation = 'Anot'
OutLogDetailed = 'Log_Detallado.txt'
OutLogAbstract = 'Log_Resumen.txt'

InGeoDBs = InGeoDBs.split(";")
ListOutAlter  = []
ListOutDelSpatialIndex = []
arcpy.env.maintainSpatialIndex = True
###########################
def GetListDSetnFC(inGeoDB):
    arcpy.AddMessage("Listando los datasets y featureclasses de la Geodatabase %s" %inGeoDB)
    arcpy.env.workspace = inGeoDB
    try:
        DictFC = {}
        for CurDset in arcpy.ListDatasets("*","Feature"):
            DictFC [CurDset] = arcpy.ListFeatureClasses("*","",CurDset)
        DictFC [''] = arcpy.ListFeatureClasses()
        DictFC [''] += arcpy.ListTables()
    except:
        arcpy.AddError('    Error recorriendo los elementos de la geodatabase. Error %s' %arcpy.GetMessages(2))
    finally:
        return DictFC
def DelDifferentFields(InFCIn, InFCOut):
    LArrFieldsCurOutAnnot = arcpy.ListFields(InFCOut)
    LArrFieldsCurOutAnnot = map(lambda x:x.name.lower(), LArrFieldsCurOutAnnot)
    LArrFieldsCurInAnnot = arcpy.ListFields(InFCIn)
    LArrFieldsCurInAnnot = map(lambda x:x.name.lower(), LArrFieldsCurInAnnot)

    def FieldFoundInsideOut(x): return not x in LArrFieldsCurOutAnnot
    def FieldFoundInsideIn(x): return not x in LArrFieldsCurInAnnot
    
    LArrDelFields = filter(FieldFoundInsideOut,LArrFieldsCurInAnnot)
    LArrDelFields += filter(FieldFoundInsideIn,LArrFieldsCurOutAnnot)
    
    if len(LArrDelFields) > 0:
        try:
            arcpy.AddMessage('        Eliminando los campos %s ..... ' % ','.join(LArrDelFields))
            arcpy.DeleteField_management(InFCIn, LArrDelFields)
            arcpy.DeleteField_management(InFCOut, LArrDelFields)
        except:
            arcpy.AddMessage('        No fue posible eliminar los campos %s. ' % ','.join(LArrDelFields))
            arcpy.AddError(arcpy.GetMessages(2))
            raise

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

def SetnSaveValuesFC():
    LCntMigratedElements = 0
    arcpy.AddMessage("        Almacenando los valores iniciales y finales de los feature IDs para insercion al consolidado ubicado en %s ....." % os.path.join(InOutGeoDB, CurDset, CurFC))
    FileOutLogDetailed.write("        Almacenando los valores iniciales y finales de los feature IDs para insercion al consolidado ubicado en %s .....\n" % os.path.join(InOutGeoDB, CurDset, CurFC))
    DictDecode = {}
    rows = arcpy.UpdateCursor(os.path.join(InOutGeoDB, CurDset, CurFC), 'FILEORIGEN' + ' IS NULL AND INOBJECTID > 0')
    for row in rows:
        LCntMigratedElements += 1
        if InAutoCreateAnnot == False:
            DictDecode [row.getValue('INOBJECTID')] = row.getValue('OBJECTID')
        row.FILEORIGEN = CurGeoDB
        rows.updateRow(row)
    try:
        del rows
        del row
    except:
        pass
    return LCntMigratedElements, DictDecode

def DecodeFeatIDAnnot():
    LCntMigratedAnnots = 0
    rows = arcpy.UpdateCursor(os.path.join(InOutGeoDB, CurDset, CurFCAnot), 'FILEORIGEN = ' + "'" + CurGeoDB + "'")
    for row in rows:
        LCntMigratedAnnots += 1
        if row.FeatureID in DictDecode.keys():
            row.FeatureID = DictDecode[row.INFEATID]
        else:
            row.FeatureID = 0
        rows.updateRow(row)
    try:
        del rows
        del row
    except:
        pass
    return LCntMigratedAnnots
def pathArcgis():
    arcgisC100=r"C:\ArcGIS\Desktop10.0\com"
    arcgisC103=r"C:\ArcGIS\Desktop10.3\com"
    arcgisP100=r"C:\Program Files (x86)\ArcGIS\Desktop10.0\com"
    arcgisP103=r"C:\Program Files (x86)\ArcGIS\Desktop10.3\com"
    Ruta=""
    if arcpy.Exists(arcgisC100):
        Ruta=arcgisC100
    elif arcpy.Exists(arcgisC103):
        Ruta=arcgisC103
    elif arcpy.Exists(arcgisP100):
        Ruta=arcgisP100
    elif arcpy.Exists(arcgisP103):
        Ruta=arcgisP103
    return Ruta  
    
def SetAutoCreateAnnot (FeatRuta, InVal = False):
    Path=pathArcgis()
    if not FeatRuta in ListOutDelSpatialIndex: 
        esriGeodatabase= GetModule(Path+os.sep+"esriGeoDatabase.olb")
        esriGeoprocessing= GetModule(Path+os.sep+"esriGeoprocessing.olb")
        esriCarto= GetModule(Path+os.sep+"esriCarto.olb")
        
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

def MapFieldRelObjectID(CurFC):
    '''Mapeo de campos para geometrias'''
    FieldMappings = arcpy.FieldMappings()
    FieldMappings.addTable(CurFC)
    FldMap_InOID = arcpy.FieldMap()
    FldMap_InOID.addInputField(CurFC, 'OBJECTID')
    Fld_InOID = FldMap_InOID.outputField
    Fld_InOID.name = 'INOBJECTID'
    FldMap_InOID.outputField = Fld_InOID

    try:
        FldMap_RuleID= arcpy.FieldMap()
        FldMap_RuleID.addInputField(CurFC, 'RULEID')
        Fld_RuleID = FldMap_RuleID.outputField
        Fld_RuleID.name = 'RULEID'
        FldMap_RuleID.outputField = Fld_RuleID
        FieldMappings.addFieldMap(FldMap_RuleID)
    except:
        pass
    FieldMappings.addFieldMap(FldMap_InOID)
    try:
        FldMap_RuleID= arcpy.FieldMap()
        FldMap_RuleID.addInputField(CurFC, 'Override')
        Fld_RuleID = FldMap_RuleID.outputField
        Fld_RuleID.name = 'Override'
        FldMap_RuleID.outputField = Fld_RuleID
        FieldMappings.addFieldMap(FldMap_RuleID)
    except:
        pass
    FieldMappings.addFieldMap(FldMap_InOID)
    
    
    return FieldMappings

def DelFields(CurFC):
    arcpy.DeleteField_management(CurFC, ['INOBJECTID', 'FILEORIGEN'])
    
def DelFieldsAnnotation(CurFCAnot):
    arcpy.DeleteField_management(CurFCAnot, ['INOBJECTID', 'INFEATID', 'FILEORIGEN'])

def AddFieldsFC(CurFC):
    arcpy.AddField_management(CurFC, 'INOBJECTID', 'LONG', '', '', '', '', 'NULLABLE')
    arcpy.AddField_management(CurFC, 'FILEORIGEN', 'TEXT', '', '', '100', '', 'NULLABLE')

def AddAndFixFieldsAnnotation(CurFCAnot, Calculate = True):
    arcpy.AddField_management(CurFCAnot, 'INOBJECTID', 'LONG', '', '', '', '', 'NULLABLE')
    arcpy.AddField_management(CurFCAnot, 'INFEATID', 'LONG', '', '', '', '', 'NULLABLE')
    arcpy.AddField_management(CurFCAnot, 'FILEORIGEN', 'TEXT', '', '', '100', '', 'NULLABLE')
    
    if Calculate:
        arcpy.CalculateField_management(CurFCAnot, 'INOBJECTID', "!OBJECTID!", "PYTHON")
        arcpy.CalculateField_management(CurFCAnot, 'INFEATID', "!FEATUREID!", "PYTHON")
        arcpy.CalculateField_management(CurFCAnot, 'FILEORIGEN', '"' + CurGeoDB + '"', "VB")

def DelSpatialIndex(CurFC):
    if not CurFC in ListOutDelSpatialIndex:
        try:
            arcpy.RemoveSpatialIndex_management(CurFC)
        except:
            pass
        finally:
            return [CurFC]
    else:
        return []
def AddFieldAnot(FcAnotIn, FcAnotOut):
    ListFieldsIn = [f.name for f in arcpy.ListFields(FcAnotIn)]
    ListFieldsOut= [f.name for f in arcpy.ListFields(FcAnotOut)]
    CamposNuevos={}
    if len(ListFieldsIn)==len(ListFieldsOut):
        pass
    if len(ListFieldsIn)<len(ListFieldsOut):
        for field in ListFieldsOut:
            if field not in ListFieldsIn:
                arcpy.AddField_management(FcAnotIn,field,"TEXT","","","50")
                CamposNuevos[FcAnotIn]=field
    if len(ListFieldsIn)>len(ListFieldsOut):
        for field2 in ListFieldsIn:
            if field2 not in ListFieldsOut:
                arcpy.AddField_management(FcAnotOut,field2,"TEXT","","","50")
                CamposNuevos[FcAnotOut]=field
    return CamposNuevos

def DelFiledsAnot(Dict):
    for k, v in Dict.iteritems():
        arcpy.DeleteField_management(k,v)


try:
    FileOutLogDetailed = open(os.path.join(os.path.dirname(InOutGeoDB), OutLogDetailed), 'a')
    FileOutLogAbstract = open(os.path.join(os.path.dirname(InOutGeoDB), OutLogAbstract), 'a')

    FileOutLogAbstract.write('Geodatabase\tDataset\tFeature_class\tElementos\tElementos_agregados\tAnotaciones\tAnotaciones_agregadas\tFecha_hora\n')
except:
    arcpy.AddMessage('Error en el registro de sucesos. El proceso se detiene')
    FileOutLogAbstract.write('Error en el registro de sucesos. El proceso se detiene\n')
    arcpy.AddError(arcpy.GetMessages(2))
    FileOutLogAbstract.write(arcpy.GetMessages(2) + '\n')
    raise
try:
    arcpy.AddMessage("Se hallaron %s geodatabase(s) para migrar" %str(len(InGeoDBs)))    
    for CurGeoDB in InGeoDBs:
        try:
            DictFC = GetListDSetnFC(CurGeoDB)
            for CurDset in sorted(DictFC.keys()):
                for CurFC in sorted(DictFC[CurDset]):
                    try:
                        IsAnnot = False
                        LCntElementsIn = int(arcpy.GetCount_management(CurFC).getOutput(0))
                        if LCntElementsIn > 0:
                            arcpy.AddMessage("    FEATURE CLASS %s (DATASET %s)" %(CurFC, CurDset))
                            FileOutLogDetailed.write("    FEATURE CLASS %s (DATASET %s)\n" %(CurFC, CurDset))
                            if arcpy.Describe(CurFC).dataType == 'FeatureClass':
                                if arcpy.Describe(CurFC).featureType != 'Annotation':
                                    if not os.path.join(InOutGeoDB, CurDset, CurFC) in ListOutAlter:
                                        arcpy.AddMessage("        Agregando y mapeando campos para el control de archivos de entrada y valores iniciales de OBJECTIDs en la GEODB de salida %s ....." %InOutGeoDB)
                                        FileOutLogDetailed.write("        Agregando y mapeando campos para el control de archivos de entrada y valores iniciales de OBJECTIDs en la GEODB de salida %s .....\n" %InOutGeoDB)
                                        ListOutAlter += [os.path.join(InOutGeoDB, CurDset, CurFC)]
                                        AddFieldsFC(os.path.join(InOutGeoDB, CurDset, CurFC))
                            
                                    FieldMappings = MapFieldRelObjectID(CurFC)

                                    DictDecode = {}
                                    CurFCAnot = CurFC + '_' + SufixAnnotation
                                    if arcpy.Exists(CurFCAnot):
                                        try:
                                            SetAutoCreateAnnot(os.path.join(InOutGeoDB, CurDset, CurFCAnot), InAutoCreateAnnot)
                                            ListOutDelSpatialIndex += DelSpatialIndex(os.path.join(InOutGeoDB, CurDset, CurFC))
                                            arcpy.AddMessage("        Realizando la insercion de geometrias a %s ....." %os.path.join(InOutGeoDB, CurDset, CurFC))
                                            FileOutLogDetailed.write("        Realizando la insercion de geometrias a %s .....\n" %os.path.join(InOutGeoDB, CurDset, CurFC))
                                            arcpy.Append_management(CurFC, os.path.join(InOutGeoDB, CurDset, CurFC), "NO_TEST", FieldMappings, '')
                                            LCntMigratedElements, DictDecode = SetnSaveValuesFC()

                                            LCntAnnotsIn = int(arcpy.GetCount_management(CurFCAnot).getOutput(0))
                                            LCntMigratedAnnots = 0 

                                            if LCntAnnotsIn > 0 and InAutoCreateAnnot == False: 
                                                IsAnnot = True
                                                AddAndFixFieldsAnnotation(CurFCAnot, True)
                                                if not os.path.join(InOutGeoDB, CurDset, CurFCAnot) in ListOutAlter:
                                                    ListOutAlter += [os.path.join(InOutGeoDB, CurDset, CurFCAnot)]
                                                    AddAndFixFieldsAnnotation(os.path.join(InOutGeoDB, CurDset, CurFCAnot), False)
                                                    ListOutDelSpatialIndex += DelSpatialIndex(os.path.join(InOutGeoDB, CurDset, CurFCAnot))
                                                
                                                #DelDifferentFields(CurFCAnot, os.path.join(InOutGeoDB, CurDset, CurFCAnot))

                                                arcpy.AddMessage("        Realizando la insercion de las anotaciones a %s ....." % os.path.join(InOutGeoDB, CurDset, CurFCAnot))
                                                FileOutLogDetailed.write("        Realizando la insercion de las anotaciones a %s ..... \n" % os.path.join(InOutGeoDB, CurDset, CurFCAnot))
                                                FiledsTemp=AddFieldAnot(CurFCAnot, os.path.join(InOutGeoDB, CurDset, CurFCAnot))
                                                arcpy.Append_management(CurFCAnot, os.path.join(InOutGeoDB, CurDset, CurFCAnot), 'TEST', '','')
                                                DelFiledsAnot(FiledsTemp)
                                                LCntMigratedAnnots = DecodeFeatIDAnnot()
                                                DelFieldsAnnotation(CurFCAnot)
                                                DelFieldsAnnotation(os.path.join(InOutGeoDB, CurDset, CurFCAnot))
                                                r = time.localtime()

                                            FileOutLogAbstract.write(CurGeoDB + '\t' + CurDset + '\t' + CurFC + '\t' + str(LCntElementsIn) + '\t' + str(LCntMigratedElements) + '\t'  + str(LCntAnnotsIn) + '\t'  + str(LCntMigratedAnnots) + '\t' + '{0}/{1}/{2} {3}:{4}\n'.format(r[0], str(r[1]).zfill(2), str(r[2]).zfill(2), str(r[3]).zfill(2), str(r[4]).zfill(2)))
                                            FileOutLogAbstract.flush()
                                            DelFields(CurFC)
                                            DelFields(os.path.join(InOutGeoDB, CurDset, CurFC))
                                        except:
                                            arcpy.AddMessage('    Error en algun paso involucrado en la carga de un feature class con anotaciones vinculadas. El proceso no se detiene')
                                            arcpy.AddError(arcpy.GetMessages(2))
                                            raise
                                    else:
                                        ListOutDelSpatialIndex += DelSpatialIndex(os.path.join(InOutGeoDB, CurDset, CurFC))
                                        LCntElementsIn = int(arcpy.GetCount_management(CurFC).getOutput(0))
                                        arcpy.AddMessage('        Agregando elementos a %s....' %os.path.join(InOutGeoDB, CurDset, CurFC))
                                        FileOutLogDetailed.write('        Agregando elementos a %s....\n' %os.path.join(InOutGeoDB, CurDset, CurFC))
                                        arcpy.Append_management(CurFC, os.path.join(InOutGeoDB, CurDset, CurFC), "NO_TEST", FieldMappings, '')
                                        LCntMigratedElements, DictDecode = SetnSaveValuesFC()
                                        r = time.localtime()
                                        DelFields(CurFC)
                                        DelFields(os.path.join(InOutGeoDB, CurDset, CurFC))
                                        FileOutLogAbstract.write(CurGeoDB + '\t' + CurDset + '\t' + CurFC + '\t' + str(LCntElementsIn) + '\t' + str(LCntMigratedElements) + '\t'  + str(0)+ '\t'  + str(0)  + '\t' + '{0}/{1}/{2} {3}:{4}\n'.format(r[0], str(r[1]).zfill(2), str(r[2]).zfill(2), str(r[3]).zfill(2), str(r[4]).zfill(2)))
                                        FileOutLogAbstract.flush()
                            elif arcpy.Describe(CurFC).dataType == 'Table':
                                LCntElementsIn = int(arcpy.GetCount_management(CurFC).getOutput(0))
                                if CurDset == '':
                                    arcpy.AddMessage('        Agregando elementos a %s....' %os.path.join(InOutGeoDB, CurFC))
                                    FileOutLogDetailed.write('        Agregando elementos a %s....\n' %os.path.join(InOutGeoDB, CurFC))
                                    arcpy.Append_management(CurFC, os.path.join(InOutGeoDB, CurFC), "NO_TEST")
                                    LCntMigratedElements, DictDecode  = SetnSaveValuesFC()
                                    r = time.localtime()
                                    FileOutLogAbstract.write(CurGeoDB + '\t' + CurDset + '\t' + CurFC + '\t' + str(LCntElementsIn) + '\t' + str(LCntMigratedElements) + '\t'  + str(0) + '\t'  + str(0) + '\t' + '{0}/{1}/{2} {3}:{4}\n'.format(r[0], str(r[1]).zfill(2), str(r[2]).zfill(2), str(r[3]).zfill(2), str(r[4]).zfill(2)))
                        else:
                            arcpy.AddMessage('    No se encuentran elementos en %s (dataset %s)' %(CurFC, CurDset))
                            FileOutLogDetailed.write('    No se encuentran elementos en %s (dataset %s)\n' %(CurFC, CurDset))
                    except:
                        arcpy.AddMessage('    Hay errores en la carga del feature class %s. El proceso NO se detiene, intentando migrar otro feature class de la Geodatabase %s.' %(CurFC, CurGeoDB))
                        FileOutLogDetailed.write('    Hay errores en la carga del feature class %s. El proceso NO se detiene, intentando migrar otro feature class de la Geodatabase %s.\n' %(CurFC, CurGeoDB))
                        arcpy.AddWarning(arcpy.GetMessages(2))
                        FileOutLogDetailed.write(arcpy.GetMessages(2)+ '\n')
                        pass
                    #finally:
                        #if LCntElementsIn > 0 and IsAnnot:
                            #try:
                                #arcpy.AddMessage("        Borrando campos adicionales creados ....." )
                                #FileOutLogDetailed.write("        Borrando campos adicionales creados .....\n")
                                #DelFieldsAnnotation(CurFCAnot)
                            #except:
                                #pass
        except:
            arcpy.AddError('Se encontraron errores en la Geodatabase vigente %s. El proceso NO se detiene, intentando migrar otra Geodatabase')
            FileOutLogDetailed.write('Se encontraron errores en la Geodatabase vigente %s. El proceso NO se detiene, intentando migrar otra Geodatabase\n')
            if arcpy.GetMessages(2) != '':
                arcpy.AddError(arcpy.GetMessages(2))
                FileOutLogDetailed.write(arcpy.GetMessages(2) + '\n')
except:
    arcpy.AddError('Error al nivel de alguna de las geodatabases de entrada o en la geodatabase de salida. El proceso se detiene, por favor revise los mensajes de erorres para hallar la solucion')
    FileOutLogDetailed.write('Error al nivel de alguna de las geodatabases de entrada o en la geodatabase de salida. El proceso se detiene, por favor revise los mensajes de erorres para hallar la solucion\n')
    if arcpy.GetMessages(2) != '':
        arcpy.AddError(arcpy.GetMessages(2))
        FileOutLogDetailed.write(arcpy.GetMessages(2) + '\n')
finally:
############################################################################
#####################################################################################
##################################
################################################################################################
##########################################################################################################
#############
#####################################################################
##############################################
##################
####################################
################
###################################################
    try:
        FileOutLogDetailed.close()
        FileOutLogAbstract.close()
    except:
        pass



