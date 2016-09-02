import arcpy, os,sys

#FeatuareClassEntrada = sys.argv[1]
#TxtSalida= sys.argv[2]

FeatuareClassEntrada = r"X:\100K\cuadriculas25000\GRILLAS_25K.mdb\MANA_ESTE_ESTE\PLANCHAS_25K_ESTE_ESTE"
TxtSalida=r"X:\100K\cuadriculas10000\DAT_GEODESIA\25K_Este_Este.txt"
origen="ESTE_ESTE"
FileTxt = open(TxtSalida, 'w')
fields=["PL_25000","SHAPE@"]
cursor= arcpy.da.SearchCursor(FeatuareClassEntrada, fields)

for row in cursor:
    print row[0]
    FileTxt.write(row[0]+","+str(int(row[1].extent.YMax)/1000)+","+str(int(row[1].extent.XMin)/1000)+","+str(int(row[1].extent.YMin)/1000)+","+str(int(row[1].extent.XMax)/1000)+","+origen+","+"I"+"\n")

FileTxt.close()