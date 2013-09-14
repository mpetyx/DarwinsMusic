__author__ = 'mpetyx'

from SPARQLWrapper import SPARQLWrapper, JSON


def query(sparql_query):
    #openerdf repository - sesame
    sparql = SPARQLWrapper("http://192.168.2.33:8080/openrdf-sesame/repositories/Music")

    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return "No answer found :("
    else:
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


