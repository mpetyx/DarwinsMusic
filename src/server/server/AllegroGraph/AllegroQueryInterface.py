__author__ = 'mpetyx'

from rdflib import Literal, URIRef

from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.model.value import URI as FURI
from franz.openrdf.model.literal import Literal as FLiteral


class Store(object):
    def __init__(self, **confs):
        accessMode = Repository.OPEN

        self.port = str(confs.get('port', '10035'))
        self.user = confs.get('user', 'toolate')
        self.password = confs.get('password', 'toolate')
        self.dbname = confs.get('dbname', 'system')

        self.server = AllegroGraphServer(host="83.212.105.61", port=10035, user="toolate",
                                         password="toolate")
        self.catalog = self.server.openCatalog(self.dbname)

        self.repo = self.catalog.getRepository("darwinsmusic", accessMode)
        self.repo.initialize()
        self.conn = self.repo.getConnection()

    def close(self):
        self.conn.close()

    def __len__(self):
        """ Returns size of the store """
        return self.conn.size()

    def add(self, triple):
        return self.conn.add(*map(lambda x: self._format(x), triple))

    def remove(self, triple):
        return self.conn.remove(*map(lambda x: self._format(x), triple))

    def commit(self):
        return self.conn.commit()

    def triples(self, triple=(None, None, None)):
        for tri in self.conn.getStatements(*map(lambda x: self._format(x), triple)):
            s = self._rformat(tri.getSubject())
            p = self._rformat(tri.getPredicate())
            o = self._rformat(tri.getObject())
            yield (s, p, o)

    def query(self, q, initNs={}, initBindings={}):

        # prepare Namespaces
        for prefix in initNs.keys():
            self.conn.setNamespace(prefix, str(initNs[prefix]))

        query = q
        tupleQuery = self.conn.prepareTupleQuery(QueryLanguage.SPARQL, query)

        # prepare Bindings
        for var in initBindings.keys():
            tupleQuery.setBinding(var, self._format(initBindings[var]))

        for bindingSet in tupleQuery.evaluate():
            row = []
            for index in range(bindingSet.size()):
                row.append(self._rformat(bindingSet[index]))
            yield row

    def _rformat(self, v):
        if isinstance(v, FURI):
            return URIRef(v.getURI())
        if isinstance(v, FLiteral):
            if str(v.datatype) != "<None>":
                return Literal(v.toPython(), datatype=str(v.datatype))
            else:
                return Literal(v.toPython())
        else:
            return Literal(str(v))

    def _format(self, el):
        if el is None:
            return None
        elif isinstance(el, FURI) or isinstance(el, FLiteral):
            return el
        elif isinstance(el, URIRef):
            return self.conn.createURI(str(el))
        elif isinstance(el, Literal):
            return self.conn.createLiteral(str(el), datatype=str(el.datatype))
        else:
            "Defaults to literal"
            return self.conn.createLiteral(str(el))


example = Store()
# result =  example.query("select ?s {?s ?f ?g}")
# i = 0
# for row in result:
#     print i
#     print result
#     i = i + 1
#     if i> 50:
#         break


query = "select distinct ?s {?s ?d ?f} LIMIT 40"

super_query = """
PREFIX geo-pos:<http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX umbel-ac:<http://umbel.org/umbel/ac/>
    PREFIX sw-vocab:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
    PREFIX ff:<http://factforge.net/>
    PREFIX music-ont:<http://purl.org/ontology/mo/>
    PREFIX dc-term:<http://purl.org/dc/terms/>
    PREFIX om:<http://www.ontotext.com/owlim/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX pext:<http://proton.semanticweb.org/protonext#>
    PREFIX dc:<http://purl.org/dc/elements/1.1/>
    PREFIX onto:<http://www.ontotext.com/>
    PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX yago:<http://mpii.de/yago/resource/>
    PREFIX xml:<http://www.w3.org/XML/1998/namespace>
    PREFIX umbel:<http://umbel.org/umbel#>
    PREFIX pkm:<http://proton.semanticweb.org/protonkm#>
    PREFIX wordnet16:<http://xmlns.com/wordnet/1.6/>
    PREFIX owl:<http://www.w3.org/2002/07/owl#>
    PREFIX dbpediaowl:<http://dbpedia.org/ontology/>
    PREFIX wordn-sc:<http://www.w3.org/2006/03/wn/wn20/schema/>
    PREFIX nytimes:<http://data.nytimes.com/>
    PREFIX dbp-prop:<http://dbpedia.org/property/>
    PREFIX geonames:<http://sws.geonames.org/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbpedia:<http://dbpedia.org/resource/>
    PREFIX oasis:<http://psi.oasis-open.org/iso/639/#>
    PREFIX geo-ont:<http://www.geonames.org/ontology#>
    PREFIX umbel-en:<http://umbel.org/umbel/ne/wikipedia/>
    PREFIX mo:<http://purl.org/ontology/mo/>
    PREFIX bbc-pont:<http://purl.org/ontology/po/>
    PREFIX lingvoj:<http://www.lingvoj.org/ontology#>
    PREFIX ourvocab:<http://example.org/>
    PREFIX psys:<http://proton.semanticweb.org/protonsys#>
    PREFIX umbel-sc:<http://umbel.org/umbel/sc/>
    PREFIX dbp-ont:<http://dbpedia.org/ontology/>

    SELECT DISTINCT ?s ?title ?listeners ?hits ?performer ?point ?date
    WHERE {
    ?s a mo:Track.
    ?s dc-term:title ?title.
    ?s ourvocab:has_listener_count ?listeners.
    ?s ourvocab:has_playcount ?hits.
    ?s ourvocab:has_releasedate ?date.
    ?s ourvocab:has_tag "jazz".

    ?s mo:performer ?pid.

    ?pid foaf:name ?performer.

    ?pid dbp-ont:hometown ?hid.
    ?hid geo:geometry ?point.

    }"""

result = example.query(super_query)

i = 0
for row in result:
    i = i + 1
    print i
    for r in row:
        print r

    if i>30:
        break
print "the end"


# server = AllegroGraphServer("http://83.212.105.61/",'toolate','toolate')
# server = AllegroGraphServer(host='83.212.105.61', port=10035, user="toolate", password="toolate")
#
# print "connected"
# print "Available catalogs", server.listCatalogs()
# catalog = server.openCatalog()             ## default rootCatalog
# print "Available repositories in catalog '%s':  %s" % (catalog.getName(), catalog.listRepositories())
#
# accessMode=Repository.RENEW
# AG_REPOSITORY = "darwinsmusic"
# myRepository = catalog.getRepository(AG_REPOSITORY, accessMode)
# myRepository.initialize()
# conn = myRepository.getConnection()
# print "Repository %s is up!  It contains %i statements." % (
#                 myRepository.getDatabaseName(), conn.size())