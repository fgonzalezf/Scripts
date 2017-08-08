import restapi
import os
import arcpy

CapaExtent=r"D:\SGC\MTER.mdb\Invertermales\F22MTG_MAT_GEOMETRIA_CONSULTA"
CarpetaSalida=r"D:\SGC\IMAGENESMANANTIALES"

url = 'http://srvagspru.sgc.gov.co/arcgis/rest/services/MTER/Reporte_Geologico_Termales_2/MapServer'
# reference map service
mapService = restapi.MapService(url)
fields = ['ID_MANANTIAL', 'EXT']

with arcpy.da.SearchCursor(CapaExtent, fields) as cursor:
    for row in cursor:
        envelope = row[1]
        kwargs = {'layers': 'exclude: 1,3', 'layerDefs': "0:MTER.F22MTG_MAT_GEOMETRIA.ID_MANANTIAL = "+str(row[0]) + ";2:MTER.F22MTG_MAT_GEOMETRIA.ID_MANANTIAL = "+str(row[0])}

        png= CarpetaSalida+ os.sep+str(row[0])+".png"
        if not arcpy.Exists(png):
            print png
            mapService.export(png, bbox=envelope, bboxSR=mapService.spatialReference,size="546,400",dpi=96,**kwargs)
