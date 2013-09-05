__author__ = 'mpetyx'

import rdflib


def query(sparql_query):
    g = rdflib.Graph()

    gres = g.query(sparql_query)

    # for row in qres:

    return gres


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


