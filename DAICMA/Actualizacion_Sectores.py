import arcpy, os, sys
Carpeta=r"C:\Users\miltongarcia\Downloads\Actualizacion_28_5_2019"
def listGDB(carpeta):
    arcpy.env.workspace=carpeta
    ListGDB=arcpy.ListWorkspaces("*","ACCESS")
    return ListGDB

def listFeatureClass(GDB):
    arcpy.env.workspace=GDB
    datasets = arcpy.ListDatasets(feature_type='feature')
    datasets = [''] + datasets if datasets is not None else []
    FeatLs=[]
    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            path = os.path.join(arcpy.env.workspace, ds, fc)
            FeatLs.append(path)
    return FeatLs

def Campos(Feat):
    desc = arcpy.Describe(Feat)
    Lista=[]
    ListaCampos=arcpy.ListFields(Feat)
    if desc.dataType=="FeatureClass":
        print desc.shapeType
        if desc.shapeType=="Point":
            Lista.append('SHAPE@XY')
        else:
            Lista.append('SHAPE@')
    for fld in ListaCampos:
        if fld.editable==True and fld.type!="Geometry":
            Lista.append(fld.name)
    return Lista


for gdb in listGDB(Carpeta):
    print(listFeatureClass(gdb))
