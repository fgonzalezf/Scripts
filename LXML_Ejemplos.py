import arcpy,os,sys,lxml
from lxml import etree
from lxml.builder import ElementMaker
xmlns="http://www.topografix.com/GPX/1/1"
xsi="http://www.w3.org/2001/XMLSchema-instance"
schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1gpx.xsd"

version="1.1"
ns="{xsi}"

getXML = etree.Element("{" + xmlns + "}gpx", version=version , attrib={"{"+ xsi +"}schemaLocation":schemaLocation},creator="My product", nsmap={'xsi':xsi, None:xmlns})

print(etree.tostring(getXML, xml_declaration=True,standalone='Yes',encoding="UTF-8",pretty_print=True))