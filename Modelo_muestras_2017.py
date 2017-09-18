import arcpy,os, sys

Geodatabase=r"D:\SGC\muestras\Muestras.gdb"

Excel=r"D:\SGC\muestras\MuestrasTablas.xls"

hojas=["EstacionesGeologicas","DatosEstructurales",
"SeccionesDelgada","SeccionPulida","MuestraFinos",
"Concentrados","Litogeoquimica","Gravas","Suelos",
"Arcillas","EsquirlasRoca","Palinologia","Foraminiferos",
"Amonites","Bivalvos","Braquiopodos","OtroTipoFosil"]

arcpy.CreateFeatureDataset_management(Geodatabase,"Muestras","MAGNA")
PathDataset= Geodatabase+ os.sep+ "Muestras"
def crearPunto (Nombre):
    arcpy.CreateFeatureclass_management(PathDataset,Nombre,"Point")
    Rutafeature = PathDataset+ os.sep+ Nombre
    return Rutafeature



for hoja in hojas:
    print hoja
    Tabla=Geodatabase+os.sep+hoja+"Tabla"
    arcpy.ExcelToTable_conversion(Excel,Tabla,hoja)
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





