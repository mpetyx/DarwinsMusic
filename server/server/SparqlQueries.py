__author__ = 'mpetyx'

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

def query(sparql_query):

    #openerdf repository - sesame
    sparql = SPARQLWrapper("http://192.168.0.227:8080/openrdf-sesame/repositories/Music")

    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(N3)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print result

    # for row in qres:

    return results["results"]["bindings"]


def sampleQuery():

    import rdflib

    g = rdflib.Graph()

    # ... add some triples to g somehow ...
    g.parse("some_foaf_file.rdf")

    qres = g.query(
        """SELECT DISTINCT ?aname ?bname
           WHERE {
              ?a foaf:knows ?b .
              ?a foaf:name ?aname .
              ?b foaf:name ?bname .
           }""")

    for row in qres:
        print("%s knows %s" % row)

    return '''
     @prefix dc: <http://purl.org/dc/terms/> .
     <http://example.org/about>
         dc:title "Someone's Homepage"@en .
     '''


