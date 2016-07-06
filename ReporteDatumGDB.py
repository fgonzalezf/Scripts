__author__ = 'fernando.gonzalez'
import arcpy, os, sys

Carpeta = sys.argv[1]
txt= sys.argv[2]

#Carpeta = r"X:\PRUEBAS\PACHO"
#txt= r"X:\PRUEBAS\PACHO\prueba.txt"



archivo=open(txt,"w")
arcpy.env.workspace=Carpeta

ListaGDB = arcpy.ListWorkspaces("*", "Access")

for GDB in ListaGDB:
    arcpy.AddMessage(os.path.basename(GDB))
    arcpy.env.workspace=GDB
    ListaDataset = arcpy.ListDatasets()
    listaDatum=[]
    for dataset in ListaDataset:
        Des=arcpy.Describe(dataset)
        listaDatum.append(Des.spatialReference.Name)
    X=0
    tempDatum=""
    tempDatum2=""
    for datum in listaDatum:

        if X==0:
            tempDatum=datum
            X=X+1
        if X!=0:
            if tempDatum==datum:
                pass
            else:
                tempDatum2=datum

    if tempDatum2=="" and tempDatum!="":
        archivo.write(GDB +" DATUM: "+tempDatum +"\n")
    elif tempDatum2!="" and tempDatum!="":
        archivo.write(GDB +" DATUM DISTINTOS "+tempDatum +" Y"+tempDatum2+ "\n")
    else:
        archivo.write(GDB +" Vacia"+"\n")
archivo.close()







