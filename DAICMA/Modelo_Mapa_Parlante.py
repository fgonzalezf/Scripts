import arcpy,os, sys

Geodatabase=r"C:\Users\APN\Documents\APN\MapaParlante\MapaParlante.mdb"

Excel=r"C:\Users\APN\Documents\APN\MapaParlante\ModeloParlante.xls"
arcpy.env.overwriteOutput=True
#hojas=["Sitios","HitosMunicipio", "VerificacionInformacion", "RegistroNuevaInformacion","SenalesPeligro","RevisionExploracionRiesgo"]

hojas=["FichaTecnica"]

arcpy.CreateFeatureDataset_management(Geodatabase,"MapaParlante","MAGNA")
PathDataset= Geodatabase+ os.sep+ "MapaParlante"
def crearPunto(Nombre):
    arcpy.CreateFeatureclass_management(PathDataset,Nombre,"Point")
    Rutafeature = PathDataset+ os.sep+ Nombre
    return Rutafeature
def crearPoligono(Nombre):
    arcpy.CreateFeatureclass_management(PathDataset,Nombre,"Polygon")
    Rutafeature = PathDataset+ os.sep+ Nombre
    return Rutafeature
def crearTabla(Nombre):
    arcpy.CreateTable_management(Geodatabase,Nombre)
    Rutafeature = Geodatabase+ os.sep+ Nombre
    return Rutafeature

for hoja in hojas:
    print hoja
    Tabla=Geodatabase+os.sep+hoja+"Tabla"
    arcpy.ExcelToTable_conversion(Excel,Tabla,hoja)
    CapaPunto=""
    if hoja=="FichaTecnica":
        CapaPunto=crearTabla(hoja)
    elif hoja=="SenalesPeligro":
        CapaPunto=crearPoligono(hoja)
    else:
        CapaPunto=crearPunto(hoja)
    fields=["NOMBRE","ALIAS","TIPO","LONGITUD","NULO"]
    with arcpy.da.SearchCursor(Tabla, fields) as cursor:
        for row in cursor:
            Tipo=""
            if row[2].upper()=="TEXT":
                Tipo="TEXT"
            elif row[2].upper()=="DOUBLE" or row[2].upper()=="FLOAT":
                Tipo="DOUBLE"
            elif row[2].upper()=="LONG INTEGER":
                Tipo="LONG"
            elif row[2].upper() == "SHORT INTEGER":
                Tipo = "SHORT"
            elif row[2].upper() == "DATE":
                Tipo = "DATE"
            Nulo=""
            if row[4].upper() == "NO" or row[4].upper() == "":
                Nulo = "NON_NULLABLE"
            elif row[4].upper() == "YES":
                Nulo = "NULLABLE"
            Longitud=""
            if str(row[3]) =="None":
                Longitud = ""
            else:
                Longitud = str(row[3])
            print ("Capa: "+ CapaPunto)
            print ("Nombre: " + row[0])
            print ("Tipo: " + Tipo)
            print ("Longitud: " + Longitud)
            print ("Alias: " + row[1])
            print ("Nulo: " + Nulo)
            if row[0]!="":
                try:
                    arcpy.AddField_management(CapaPunto,row[0],Tipo,"","",Longitud,row[1],Nulo)
                except Exception as ex:
                    print ("Error..."+ ex.message)





