__author__ = 'mpetyx'

from rdflib import Graph, plugin
from rdflib.parser import Parser
from StringIO import StringIO
import rdfextras
rdfextras.registerplugins()

testrdfjson = '''{
"head":
    {"vars": ["count"]},
"results":
    {"bindings":
        [{"count": {"datatype": "http://www.w3.org/2001/XMLSchema#integer",
"type": "typed-literal", "value": "100351"}}]
    }
}'''

testrdfjson = '''{
        "count": {"datatype": "http://www.w3.org/2001/XMLSchema#integer",
"type": "typed-literal", "value": "100351"}
}'''

import json

temp = json.loads(testrdfjson)

# testrdfjson = testrdfjson.replace("'",'"')


# testrdfjson = '''{
#       "http://example.org/about" :
#         {
#            "http://purl.org/dc/elements/1.1/title": [
#                 { "type" : "literal" , "value" : "Anna's Homepage." }
#             ]
#         }
#     }'''

g = Graph()

g.parse(StringIO(testrdfjson), format="rdf-json")

print g.serialize(format='json-ld', indent=4)


# from rdflib.plugins.stores.sparqlstore import SPARQLStore
# import rdflib
#
# sparql2 = SPARQLStore("http://192.168.2.33:8080/openrdf-sesame/repositories/Music")
#
# # sparql2.setQuery("""
# # SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
# # """)
#
# g = rdflib.Graph(sparql2)
#
#
#
# result2 = g.query("""
# SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
# """)

# print result2