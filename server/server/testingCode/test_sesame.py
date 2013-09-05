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

sparql = SPARQLWrapper("http://192.168.2.33:8080/openrdf-sesame/repositories/Music")

sparql.setQuery("""
SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
""")

sparql.setReturnFormat(JSON)

results = sparql.query().convert()
# print results
for result in results:
    print result

g = Graph()

for triple in results:
    g.add(triple)

print g.serialize(format='json-ld', indent=4)

# curl -v -X GET  -d "query:SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}'" http://127.0.0.1:8000/sparql