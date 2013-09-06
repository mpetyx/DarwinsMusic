__author__ = 'mpetyx'


# import rdflib
# import rdfextras
#
# def query(sparql_query):
#
#     triplestore = "http://192.168.0.227:8080/openrdf-sesame/repositories/Music/"
#     store = rdfextras.store.SPARQL.SPARQLStore(triplestore)
#     g = rdflib.Graph(store)
#
#     gres = g.query(sparql_query)
#
#     return gres
#
# sparql_query = """
# SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
# """
#
# print query(sparql_query)



from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
from rdflib import Graph
from StringIO import StringIO

sparql = SPARQLWrapper("http://192.168.2.27:8080/openrdf-sesame/repositories/Music")

sparql.setQuery("""
SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
""")

sparql.setReturnFormat(XML)

results = sparql.query().convert()

g = Graph()

g.parse(StringIO(results.toxml()), format='xml')

superQuery = """

"""

# rota = g.query("""
# SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
# """)
#
# for row in rota:
#     print row
#
# print g.serialize(format='json-ld', indent=4)
# print g.serialize(format='n3', indent=4)

for triple in g:
    print triple