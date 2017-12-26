from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader

URL = 'http://srvagspru.sgc.gov.co/oairequest'

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)

client = Client(URL, registry)
X=0
for record in client.listRecords(metadataPrefix='oai_dc'):
    X=X+1
    print (str(X))+"...."
    print str(record[0].identifier())