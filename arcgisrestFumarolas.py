import restapi
import os
import arcpy

CapaExtent=r"D:\SGC\MTER.mdb\Invertermales\F22FUG_FUM_GEOMETRIA_CONSULTA"
CarpetaSalida=r"D:\SGC\IMAGENESFUMAROLAS"

url = 'http://srvagspru.sgc.gov.co/arcgis/rest/services/MTER/Reporte_Geologico_Termales_2/MapServer'
# reference map service
mapService = restapi.MapService(url)
fields = ['ID_FUMAROLA', 'EXT']

with arcpy.da.SearchCursor(CapaExtent, fields) as cursor:
    for row in cursor:
        envelope = row[1]
        kwargs = {'layers': 'exclude: 0,2', 'layerDefs': "1:MTER.F22FUG_FUM_GEOMETRIA.ID_FUMAROLA = "+str(row[0]) + ";3:MTER.F22FUG_FUM_GEOMETRIA.ID_FUMAROLA = "+str(row[0])}
        png= CarpetaSalida+ os.sep+str(row[0])+".png"
        print png
        mapService.export(png, bbox=envelope, bboxSR=mapService.spatialReference,size="546,400",dpi=96,**kwargs)
