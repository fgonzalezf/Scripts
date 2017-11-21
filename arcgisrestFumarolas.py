import restapi
import os
import arcpy

CapaExtent=r"C:\Users\Desarrollo\Documents\INVERTERMALES\datos.mdb\Invertermales\F22FUG_FUM_GEOMETRIA"
CarpetaSalida=r"F:\INVERTERMALES\Imagenes\Fumarolas"

url = 'http://srvagspru.sgc.gov.co/arcgis/rest/services/MTER/Reporte_Geologico_Termales_2/MapServer'
# reference map service
mapService = restapi.MapService(url)
fields = ['SHAPE@XY','ID_FUMAROLA']

with arcpy.da.SearchCursor(CapaExtent, fields) as cursor:
    for row in cursor:
        x, y = row[0]
        envelope = str(x-0.2)+","+str(y-0.12)+","+str(x+0.2)+","+str(y+0.12)
        kwargs = {'layers': 'exclude: 0,2', 'layerDefs': "1:MTER.F22FUG_FUM_GEOMETRIA.ID_FUMAROLA = "+str(row[1]) + ";3:MTER.F22FUG_FUM_GEOMETRIA.ID_FUMAROLA = "+str(row[1])}
        png= CarpetaSalida+ os.sep+str(row[1])+".png"
        print png
        mapService.export(png, bbox=envelope, bboxSR=mapService.spatialReference,size="540,400",dpi=96,**kwargs)
