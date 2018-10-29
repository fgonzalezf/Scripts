import arcpy, os,sys

CarpetaSalida=r""
Escala=10000
NumeroMuestra=20
Filas=5
Columnas=5

Planchas=r"C:\Users\APN\Documents\IGAC\Planchas_10K_Planas\Central.shp"
plancha="8IIIB1"
salida=r"C:\Users\APN\Documents\IGAC\Prueba.shp"
arcpy.env.overwriteOutput=True
def QueryPlancha (Feat, plancha):
    fields=['SHAPE@WKT',"PLANCHA","SHAPE@"]
    with arcpy.da.SearchCursor(Feat, fields, """PLANCHA="""+"'"+plancha+"'") as cursor:
        for row in cursor:
            print(int(round(row[2].extent.XMin)))
            print(int(round(row[2].extent.YMin)))
            print(int(round(row[2].extent.XMax)))
            print(int(round(row[2].extent.YMax)))
            print(row[2])

            return ([int(round(row[2].extent.XMin)),int(round(row[2].extent.YMin)),int(round(row[2].extent.XMax)),int(round(row[2].extent.YMax))])

def CreateFishnet(coordenadas, featOut, filas, columnas):
    Largo = (coordenadas[2] - coordenadas[0])
    Alto = (coordenadas[3] - coordenadas[1])
    LargoFish = (coordenadas[2]-coordenadas[0])/columnas
    AltoFish =(coordenadas[3]-coordenadas[1])/filas
    features = []
    for i in range(filas):
        YminFish=coordenadas[1]+(AltoFish*i)
        YmaxFish = coordenadas[1] + AltoFish+ (AltoFish*i)
        for j in range(columnas):
            XminFish = coordenadas[0] + (LargoFish * j)
            XmaxFish = coordenadas[0] + LargoFish+ (LargoFish * j)
            features.append(arcpy.Polygon
                            (arcpy.Array([
                                            arcpy.Point(XminFish,YminFish),
                                            arcpy.Point(XmaxFish,YminFish),
                                            arcpy.Point(XmaxFish,YmaxFish),
                                            arcpy.Point(XminFish,YmaxFish)])))
    arcpy.CopyFeatures_management(features, featOut)


coord=QueryPlancha(Planchas,plancha)
CreateFishnet(coord,salida,Filas,Columnas)