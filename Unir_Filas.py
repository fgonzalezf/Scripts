__author__ = 'fernando.gonzalez'
import arcpy, os, sys
reload(sys)
sys.setdefaultencoding("utf-8")

tablaEntrada=sys.argv[1]
tablaSalida = sys.argv[2]
arcpy.env.overwriteOutput=True
arcpy.CreateTable_management(os.path.dirname(tablaSalida),os.path.basename(tablaSalida),tablaEntrada)


rows = arcpy.SearchCursor(tablaEntrada)
uniqueValue={}

for row in rows:
    uniqueValue[row.getValue ("poi_pvid")]="valor"

rowsIns = arcpy.InsertCursor(tablaSalida)

for key,value in uniqueValue.items():
    rowsq = arcpy.SearchCursor(tablaEntrada, "poi_pvid = "+str(key) )
    rowin = rowsIns.newRow()
    tel=""
    email=""
    pagina=""
    codigo=""
    try:
        for rowq in rowsq:

            if "@" in str(rowq.contact_info):
                if email=="":
                    email=str(rowq.contact_info)
                else:
                    email=email+","+str(rowq.contact_info)
            elif "http".upper() in str(rowq.contact_info).upper():
                if pagina=="":
                    pagina=str(rowq.contact_info)
                else:
                    pagina=pagina+","+str(rowq.contact_info)
            else:
                if tel=="":
                    tel=str(rowq.contact_info)
                else:
                    tel=tel+","+str(rowq.contact_info)
            if codigo=="":
                fields= arcpy.ListFields(tablaEntrada)
                for field in fields:
                    if field.name !="Web" and field.name !="Phone" and field.name !="Email" and field.name !="OBJECTID":
                        rowin.setValue(field.name, rowq.getValue(field.name))

                codigo=str(rowq.poi_pvid)

        rowin.Phone=tel
        rowin.Email=email
        rowin.Web=pagina
        rowsIns.insertRow(rowin)
        arcpy.AddMessage(str(key))
    except Exception as e:
        arcpy.AddMessage( "**********Error******** en el ID: "+ str(key) + "****" +e.message)
