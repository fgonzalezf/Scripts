import csv
import time
from IPython.display import display, HTML
import json
#import pandas
import logging
log = logging.getLogger()

from arcgis.mapping import WebMap
from arcgis.mapping import WebScene
from arcgis.gis import GIS

gis = GIS("https://ergit.presidencia.gov.co/arcpre/home", "adminportal", "Cartografia17")

CHECK_ALL_ITEMS = True
CHECK_WEBMAPS = True
CHECK_WEBSCENES = True
CHECK_APPS = True
def get_items_to_check():
    """Generator function that will yield Items depending on how you
    configured your notebook. Will either yield every item in an
    organization, or will yield items in specific groups.
    """
    if CHECK_ALL_ITEMS:
        for user in gis.users.search():
            for item in user.items(max_items=999999999):
                # For the user's root folder
                yield item
            for folder in user.folders:
                # For all the user's other folders
                for item in user.items(folder, max_items=999999999):
                    yield item
    else:
        for group_name in CHECK_THESE_GROUPS:
            group = gis.groups.search(f"title: {group_name}")[0]
            for item in group.content():
                yield item

for item in get_items_to_check():
    if item.type=="Web Map":
        print(item.title)