__author__ = 'mpetyx'


import rdflib


def query(sparql_query):

    triplestore = "http://192.168.0.128:8080/openrdf-sesame/repositories/Music/"
    g = rdflib.Graph()

    gres = g.query(sparql_query)

    return gres

sparql_query = """
SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
"""

print query(sparql_query)