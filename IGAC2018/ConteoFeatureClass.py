import arcpy, os,sys

Geodatabase=sys.argv[1]
arcpy.env.workspace=Geodatabase

ListaFeatOut=arcpy.ListFeatureClasses()
ListaDatasets=arcpy.ListDatasets("*","Feature")
boolFeatures=sys.argv[2]
boolAnotacion=sys.argv[3]
Archivo_TXT=sys.argv[4]
f=open(Archivo_TXT ,"w")

for fc in ListaFeatOut:
    Describe = arcpy.Describe(fc)
    if Describe.FeatureType == "Simple" and boolFeatures == "true":
        result = arcpy.GetCount_management(fc)
        count = int(result.getOutput(0))
        f.write("Feature Class: ...." + fc+ "...."+ "Numero de Registros: "+str(count)+"\n")
        arcpy.AddMessage(fc)
    print fc

for Dataset in ListaDatasets:

    DatasetOut= Geodatabase+os.sep+Dataset
    arcpy.env.workspace=DatasetOut
    ListaFeat= arcpy.ListFeatureClasses()
    for fc in ListaFeat:
        Describe = arcpy.Describe(fc)
        if Describe.FeatureType=="Simple" and boolFeatures=="true":
            result = arcpy.GetCount_management(fc)
            count = int(result.getOutput(0))
            if count > 0:
                f.write("Feature Class:  ....    " +fc + "    "+ "Numero de Registros:  ... "+str(count)+"\n")
                arcpy.AddMessage(fc)
        if Describe.FeatureType=="Annotation" and boolAnotacion=="true":
            result = arcpy.GetCount_management(fc)
            count = int(result.getOutput(0))
            if count > 0:
                f.write("Feature Class Anotacion:  ....  " + fc+ "     "+ "Numero de Registros:  ... "+str(count) +"\n")
                arcpy.AddMessage(fc)
f.close()

