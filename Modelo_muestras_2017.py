import arcpy,os, sys
reload(sys)
sys.setdefaultencoding("utf-8")

#Geodatabase=r"C:\Users\APN\Documents\SGC\Muestras\Muestras.gdb"
Geodatabase=sys.argv[1]
#Excel=r"C:\Users\APN\Documents\APN\Visores\MuestrasTablas_Fernando_10_10_17_Final.xls"
Excel = sys.argv[2]
arcpy.env.overwriteOutput=True
#hojas = sys.argv[3].split(";")
dataset=sys.argv[3]
sistemaref=sys.argv[4]
tipoGeometria=sys.argv[5]
#hojas=["EstacionesGeologicas","DatosEstructurales",
#"SeccionDelgada","SeccionPulida","MuestraFinos",
#"ConcentradosBatea","AnalisisQuimicoRocaTotal","Gravas","Suelos",
#"Arcillas","EsquirlasRoca","Palinologia","Foraminiferos",
#"Amonites","Bivalvos","Braquiopodos","OtroTipoFosil"]

arcpy.CreateFeatureDataset_management(Geodatabase,dataset,sistemaref)
PathDataset= Geodatabase+ os.sep+ dataset
def crearPunto(Nombre):
    if tipoGeometria!="table":
        arcpy.CreateFeatureclass_management(PathDataset,Nombre,tipoGeometria)
        Rutafeature = PathDataset+ os.sep+ Nombre
    else:
        arcpy.CreateTable_management(Geodatabase,Nombre)
        Rutafeature = Geodatabase+ os.sep + Nombre
    return Rutafeature

def getSheetName(file_name):
    pointSheetObj = []
    import xlrd as xl
    TeamPointWorkbook = xl.open_workbook(file_name)
    pointSheets = TeamPointWorkbook.sheet_names()

    for i in pointSheets:
        pointSheetObj.append(tuple((TeamPointWorkbook.sheet_by_name(i),i))[1])
    return pointSheetObj

hojas = getSheetName(Excel)
for hoja in hojas:
    print hoja
    if hoja[:4] != "Dom_":
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
                arcpy.AddMessage("Capa: "+ CapaPunto)
                arcpy.AddMessage("Nombre: " + row[0])
                arcpy.AddMessage ("Tipo: " + Tipo)
                arcpy.AddMessage ("Longitud: " + Longitud)
                arcpy.AddMessage ("Alias: " + row[1])
                arcpy.AddMessage ("Nulo: " + Nulo)
                if row[0]!="":
                    try:
                        arcpy.AddField_management(CapaPunto,row[0],Tipo,"","",Longitud,row[1],Nulo)
                    except Exception as ex:
                        arcpy.AddError ("Error..."+ ex.message)

        arcpy.Delete_management(Tabla)
    else:
        Tabla = Geodatabase + os.sep + hoja + "Tabla"
        arcpy.ExcelToTable_conversion(Excel, Tabla, hoja)
        arcpy.TableToDomain_management(Tabla,"Coded","Description",Geodatabase,hoja)
        arcpy.Delete_management(Tabla)






