
from lxml.builder import ElementMaker
from lxml import etree as et
import base64

XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'
  
class OAIDC(object):
    """The standard OAI Dublin Core metadata format.
    
    Every OAI feed should at least provide this format.

    It is registered under the name 'oai_dc'
    """
    
    def __init__(self, prefix, config, db):
        self.prefix = prefix
        self.config = config
        self.db = db

        self.ns = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                   'dc':'http://purl.org/dc/elements/1.1/'}
        self.schemas = {
            'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd'}
        
    def get_namespace(self):
        return self.ns[self.prefix]

    def get_schema_location(self):
        return self.schemas[self.prefix]
    
    def __call__(self, element, metadata):

        data = metadata.record
        
        OAI_DC =  ElementMaker(namespace=self.ns['oai_dc'],
                               nsmap =self.ns)
        DC = ElementMaker(namespace=self.ns['dc'])

        oai_dc = OAI_DC.dc()
        oai_dc.attrib['{%s}schemaLocation' % XSI_NS] = '%s %s' % (
            self.ns['oai_dc'],
            self.schemas['oai_dc'])

        for field in ['title',
            'date',
            'dateType',
			#'description',
			'abstract',
            'creator',
            'role',
            'contributor',
            'city',
            'administrativeArea',
            'postalCode',
            'country',
            'electronicMailAddress',
            'voice',
            'spatialRepresentationType',
            'denominator',
            'distance',
            'language',
            'characterSet',
            'topicCategory',
            'description1',
            'westBoundLongitude',
            'eastBoundLongitude',
            'southBoundLatitude',
            'northBoundLatitude',
            'date1',
            'date2',
            'purpose',
            'source',
            'title1',
            'description2',
            'description3',
            'date3',
            'date4',
            'Depart',
            'Municip',
            'PlancIGAC',
            'EstadProyect',
            'PorcentComplet',
            'AreaConocim',
            'LineaTemat',
            'EscalaProy',
            'type',
            'TipoResult',
            'status',
            'maintenanceAndUpdateFrequency',
            'maintenanceNote',
            'fileName',
            'type2',
            'subject',
            'VistConcep',
            'rights',
            'accessConstraints',
            'useConstraints' ,
            'otherConstraints' ,
            'classification' ,
            'usernote' ,
            'source1' ,
            'associationType' ,
            'relation' ,
            'level' ,
            'dataset' ,
            'statement' ,
            'description4' ,
            'descriptionReferenceSystem' ,
            'prodImpr' ,
            'format' ,
            'version' ,
            'publisher' ,
            'role1' ,
            'deliveyPoint1' ,
            'city1' ,
            'administrativeArea1' ,
            'postalCode1' ,
            'country1' ,
            'electronicMailAddress1' ,
            'voice1' ,
            'fees' ,
            'identifier' ,
            'protocol' ,
            'name1' ,
            'description5' ,
            'datestamp' ,
            'identifier1' ,
            'path' ,
            'language1' ,
            'characterSet1' ,
            'publisher1' ,
            'role2' ,
            'deliveyPoint2' ,
            'city2' ,
            'administrativeArea2' ,
            'postalCode2' ,
            'country2' ,
            'electronicMailAddress2' ,
            'voice2' ,
            'metadataStandardName' ,
            'metadataStandardVersion' ,
            'accessConstraints1' ,
            'useConstraints1' ,
            'otherConstraints1' ,
            'classification1' ,
            'NombrMedMet' ,
            'DescripMedidMet' ,
            'TipEvaluaMet' ,
            'DescMetEvMet' ,
            'datestamp1' ,
            'ValorMetad' ,
            'UnidadMedValMet' ,
            'NombMedMet' ,
            'DescripMedidMetConsLog' ,
            'TipEvaluaMetConsDom' ,
            'DescripMetEvConsDom' ,
            'datestamp2' ,
            'url' ,
	    'BusqPredef']:
            el = getattr(DC, field)
            try:
                for value in data['metadata'].get(field, []):
                    # <editor-fold desc="Description">
                    #and data['metadata'].get('url')
                    # </editor-fold>
		            #if field == 'identifier' :
		            #value = data['metadata']['url'][0]
                    if field != 'source':
                            oai_dc.append(el(value))
            except AttributeError:
                pass
        source_element = et.fromstring(et.tostring(oai_dc))
        value=source_element
        el = getattr(DC, "source")
        metstring= base64.b64encode(et.tostring(value))
        oai_dc.append(el(metstring))

        element.append(oai_dc)
        print ("Metadato oaidc")