import restapi
import os
import arcpy

CapaExtent=r"D:\SGC\MTER.mdb\Invertermales\F22MTG_MAT_GEOMETRIA_CONSULTA"
CarpetaSalida=r"D:\SGC\IMAGENESMANANTIALES"

url = 'http://srvags.sgc.gov.co/arcgis/rest/services/MTER/Reporte_Geologico_Termales/MapServer'
# reference map service
mapService = restapi.MapService(url)
fields = ['ID_MANANTIAL', 'EXT']

with arcpy.da.SearchCursor(CapaExtent, fields) as cursor:
    for row in cursor:
        envelope = row[1]
        png= CarpetaSalida+ os.sep+str(row[0])+".png"
        print png
        mapService.export(png, bbox=envelope, bboxSR=mapService.spatialReference,size="273,200")
