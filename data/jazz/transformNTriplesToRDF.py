__author__ = 'mpetyx'



from rdflib import Graph

g = Graph()

g.parse('triples.nt',format='n3')
example = open("triples.rdf","w")
example.write(g.serialize(format='xml'))
example.close()