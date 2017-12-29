import arcpy, os,sys

#FeatuareClassEntrada = sys.argv[1]
#TxtSalida= sys.argv[2]

FeatuareClassEntrada = r"D:\Pruebas\Grilla_25_Geograficas\Grilla_25_Geografica_MAGNA.shp"
TxtSalida=r"D:\Pruebas\Grilla_25_Geograficas\25k_MAGNA.txt"
origen="MAGNA"
FileTxt = open(TxtSalida, 'w')
fields=["PLANCHA","SHAPE@"]
cursor= arcpy.da.SearchCursor(FeatuareClassEntrada, fields)

for row in cursor:
    print row[0]
    FileTxt.write(row[0]+","+str(float(row[1].extent.YMax))+","+str(float(row[1].extent.XMin))+","+str(float(row[1].extent.YMin))+","+str(float(row[1].extent.XMax))+","+origen+","+"I"+"\n")

FileTxt.close()