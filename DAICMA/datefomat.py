import arcpy
from datetime import datetime
fc = r"E:\Scripts\GDB_ZONAS\CENAM_BK.gdb\CENAM\Accidentes"
rows = arcpy.SearchCursor(fc)
for row in rows:
    datetimeVal = row.getValue("FECHA___DD_MM_AAAA_")
    formattedTime = datetime.strftime(datetimeVal, "%d/%m/%Y")
    print formattedTime