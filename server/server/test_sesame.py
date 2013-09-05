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
sparql = SPARQLWrapper("http://192.168.0.227:8080/openrdf-sesame/repositories/Music")

sparql.setQuery("""
SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print result["count"]["value"]