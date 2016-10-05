import arcpy,os,sys,lxml
from lxml import etree
from lxml.builder import ElementMaker
xmlns="http://www.topografix.com/GPX/1/1"
xsi="http://www.w3.org/2001/XMLSchema-instance"
schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1gpx.xsd"

version="1.1"
#ns="{xsi}"
ns = {
                   'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                   'dc':'http://purl.org/dc/elements/1.1/'}
getXML = etree.Element("{" + xmlns + "}gpx", version=version , attrib={"{"+ xsi +"}schemaLocation":schemaLocation},creator="My product", nsmap={'xsi':xsi})

print(etree.tostring(getXML, xml_declaration=True,standalone='Yes',encoding="UTF-8",pretty_print=True))


from lxml.builder import ElementMaker
from lxml import etree, objectify
XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'
ns = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/','dc':'http://purl.org/dc/elements/1.1/'}
schemas = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd'}

OAI_DC =  ElementMaker(namespace=ns['oai_dc'],nsmap =ns)
oai_dc = OAI_DC.dc()
oai_dc.attrib['{%s}schemaLocation' % XSI_NS] = '%s %s' % (ns['oai_dc'],schemas['oai_dc'])
print(etree.tostring(oai_dc,pretty_print=True))