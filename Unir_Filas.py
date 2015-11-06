__author__ = 'fernando.gonzalez'
import arcpy, os, sys

tablaEntrada=r"X:\PRUEBAS\UnirFilas\prueba3.mdb\TablaEntrada"
tablaSalida = r"X:\PRUEBAS\UnirFilas\Prueba3.mdb\TablaSalida"
arcpy.env.overwriteOutput=True
arcpy.CreateTable_management(os.path.dirname(tablaSalida),os.path.basename(tablaSalida),tablaEntrada)


rows = arcpy.SearchCursor(tablaEntrada)
uniqueValue={}
uniqueValue["not"]="valor"
for row in rows:
    uniqueValue[row.getValue ("codigo")]="valor"

rowsIns = arcpy.InsertCursor(tablaSalida)

for key,value in uniqueValue.items():

    rowsq = arcpy.SearchCursor(tablaEntrada,"[Codigo]= '"+str(key)+"'")
    rowin = rowsIns.newRow()
    tel=""
    email=""
    pagina=""
    codigo=""
    for rowq in rowsq:
        if "@" in str(rowq.ContacInfo):
            if email=="":
                email=str(rowq.ContacInfo)
            else:
                email=email+","+str(rowq.ContacInfo)
        elif "http" in str(rowq.ContacInfo):
            if pagina=="":
                pagina=str(rowq.ContacInfo)
            else:
                pagina=pagina+","+str(rowq.ContacInfo)
        else:
            if tel=="":
                tel=str(rowq.ContacInfo)
            else:
                tel=tel+","+str(rowq.ContacInfo)
        if codigo=="":
            codigo=rowq.Codigo

    rowin.Telefono=tel
    rowin.IMAIL=email
    rowin.Pagina=pagina
    rowin.Codigo=codigo
    rowsIns.insertRow(rowin)
    print str(email)
del rowin,rowsIns
del row,rows








