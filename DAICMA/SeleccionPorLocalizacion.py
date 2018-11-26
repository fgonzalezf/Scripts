import arcpy, os,sys

poligonoSeleccion=r"C:\Users\APN\Documents\GDB\Scripts\GDB\Antioquia.shp"
datasetEntrada=r"C:\Users\APN\Documents\APN\GDB\Scripts\GDB\Bk_GDB.gdb\DAICMA"
carpetaSalida=r"C:\Users\APN\Documents\GDB\Scripts\GDB\Antioquia"
reload(sys)
sys.setdefaultencoding("iso-8859-1")
arcpy.env.workspace=datasetEntrada
listaFeat= arcpy.ListFeatureClasses()

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})
def Campos(Feat):
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name)
    return Lista

for fc in listaFeat:
    arcpy.AddMessage(fc)
    LayerSeleccion = arcpy.MakeFeatureLayer_management(fc, "layerSeleccion")
    seleccion = arcpy.SelectLayerByLocation_management(LayerSeleccion,"INTERSECT",poligonoSeleccion,"-10 Meters")
    result = arcpy.GetCount_management(seleccion)
    count = int(result.getOutput(0))
    if count>0:
        arcpy.FeatureClassToFeatureClass_conversion(seleccion,carpetaSalida,fc+".shp")
        shapeFileSalida=carpetaSalida + os.sep +fc+".shp"
        #Borrar Campos Null
        listaCampos= Campos(shapeFileSalida)
        for campo in listaCampos:
            valores=unique_values(shapeFileSalida,campo)
            if len(valores)==1 and count>1 and (valores[0]==0 or valores[0]==None or valores[0]==' ' or valores[0]==''):
                arcpy.DeleteField_management(shapeFileSalida,campo)
    arcpy.Delete_management(LayerSeleccion)


