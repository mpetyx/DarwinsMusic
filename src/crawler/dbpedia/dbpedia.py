from SPARQLWrapper import SPARQLWrapper, JSON
from os.path import basename, abspath, exists
from numpy import unique
from glob import glob
from time import time
import pickle
import json

#TODO - 1
#In these functions, we need to work out the cases which have more than
#one result. For now, I consider the first hit!

#TODO - 2
#Get influence relations

class dbpedia:
    def __init__(self, delay = 0.5):
        """
        Initiates sparql interface to DBPedia.
        """
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
        self.delay = delay
        self.lastRequest = time()

    def wait(self):
        actualDelay = time() - self.lastRequest
        if actualDelay < self.delay: sleep(actualDelay)
        self.lastRequest = time()
    
    def getBand(self, name):
        """
        Gets band information from DBPedia, given the name of a band.
        """

        self.sparql.setQuery("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX : <http://dbpedia.org/resource/>
        PREFIX dbpedia2: <http://dbpedia.org/property/>
        PREFIX dbpedia: <http://dbpedia.org/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
        PREFIX dbpprop: <http://dbpedia.org/property/>
        PREFIX dbres: <http://dbpedia.org/resource/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

        SELECT ?artist, ?careerStartYear, ?hometown, ?hometownName, ?coordinates WHERE {
         ?artist rdf:type <http://schema.org/MusicGroup> .
         ?artist foaf:name "%s"@en .
         OPTIONAL { ?artist dbpedia-owl:activeYearsStartYear ?startYear }
         OPTIONAL { ?artist dbpedia-owl:hometown ?hometown }
         OPTIONAL { ?hometown foaf:name ?hometownName }
         OPTIONAL { ?hometown geo:geometry ?coordinates }
         }
        limit 2
        """%name)

        self.sparql.setReturnFormat(JSON)

        self.wait()

        results = self.sparql.query().convert()

        if results['results']['bindings'] == []:
            return None
        else:
            results = results['results']['bindings'][0]
            results['artist']['type'] = 'band'
        return results


    def getArtist(self, name):
        """
        Gets artist information from DBPedia, given the name of a band.
        """

        self.sparql.setQuery("""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX : <http://dbpedia.org/resource/>
        PREFIX dbpedia2: <http://dbpedia.org/property/>
        PREFIX dbpedia: <http://dbpedia.org/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
        PREFIX dbpprop: <http://dbpedia.org/property/>
        PREFIX dbres: <http://dbpedia.org/resource/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

        SELECT ?artist, ?careerStartYear, ?hometown, ?hometownName, ?coordinates WHERE {
         ?artist rdf:type dbpedia-owl:MusicalArtist .
         ?artist foaf:name "%s"@en .
         OPTIONAL { ?artist dbpedia-owl:activeYearsStartYear ?careerStartYear }
         OPTIONAL { ?artist dbpedia-owl:birthPlace ?hometown }
         OPTIONAL { ?hometown foaf:name ?hometownName }
         OPTIONAL { ?hometown geo:geometry ?coordinates }
         }

        limit 2
        """%name)

        self.sparql.setReturnFormat(JSON)

        self.wait()
        
        results = self.sparql.query().convert()

        if results['results']['bindings'] == []:
            results = self.getBand(name)
            return results

        results = results['results']['bindings'][0]
        results['artist']['type'] = 'artist'
        return results

