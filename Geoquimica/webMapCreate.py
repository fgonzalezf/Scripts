import os
import json
from IPython.display import display
import arcgis
from arcgis.gis import GIS
from arcgis.mapping import WebMap, WebScene

# connect to your GIS
# Create an anonymous connection to ArcGIS Online to search for contents
gis1 = GIS()
# Create a connection to your portal for publishing
gis2 = GIS("http://sgcolombiano.maps.arcgis.com", "fgonzalezf_SGColombiano", "Maidenfgf1")



wm = WebMap()
wm.definition


lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/0")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/1")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/114")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/115")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/116")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/117")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/118")
wm.add_layer(lyr)
lyr=arcgis.gis.Layer("https://srvags.sgc.gov.co/arcgis/rest/services/Atlas_Geoquimico_V2018/Atlas_Geoquimico_de_Colombia_V2018/MapServer/119")
wm.add_layer(lyr)


web_map_properties = {'title':'1_AG_Plata_Concentración en sedimentos µg/kg',
                     'snippet':'Concentracion de Sedimentos',
                     'tags':'Geoquimica'}

# Call the save() with web map item's properties.
web_map_item = wm.save(item_properties=web_map_properties)
web_map_item