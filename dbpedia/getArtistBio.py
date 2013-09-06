__author__ = "gopalkoduri"

from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF, logging
import json
from os.path import basename, abspath, exists
from glob import glob
from SPARQLWrapper import SPARQLWrapper, JSON
from numpy import unique
import pickle

sparql = SPARQLWrapper("http://dbpedia.org/sparql/")

MusicOntology = Namespace('http://purl.org/ontology/mo/')
DC = Namespace("http://purl.org/dc/terms/")
OurVocab = Namespace('http://example.org/')
foaf = Namespace("http://xmlns.com/foaf/0.1/")
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
dbpediaowl = Namespace("http://dbpedia.org/ontology/")

storefn = abspath('../data/rock/tracks.n3')
storeuri = 'file://' + storefn

class Store:
    def __init__(self):
        self.graph = ConjunctiveGraph()
        if exists(storefn):
            self.graph.load(storeuri, format='n3')
        self.graph.bind('mo', MusicOntology)
        self.graph.bind('ourvocab', OurVocab)
        self.graph.bind('dc', DC)
        self.graph.bind('foaf', foaf)
        self.graph.bind('geo', geo)
        self.graph.bind('dbpediaowl', dbpediaowl)
        self.graph.bind('rev', 'http://purl.org/stuff/rev#')

    def save(self):
        self.graph.serialize(storeuri, format='n3')

    def addArtistBio(self, trackMBID, artistData, trackData):
        trackuri = URIRef('http://musicbrainz.org/recording/%s#_' % trackMBID)

        #If there is no mbid, it means there is no earlier artist entry in triplestore
        if trackData['artist']['mbid'] == '':
            artisturi = URIRef(artistData['artist']['value'].encode('utf-8'))
            if artistData['artist']['type'] == 'artist':
                self.graph.add((artisturi, RDF.type, MusicOntology.MusicArtist))
            else:
                self.graph.add((artisturi, RDF.type, MusicOntology.MusicGroup))
            self.graph.add((trackuri, MusicOntology.performer, artisturi))
            self.graph.add((artisturi, foaf.name, Literal(trackData['artist']['name'].encode('utf-8'))))

        #if there is an artist entry, make sure the artist/band association is appropriate
        else:
            artisturi = URIRef('http://musicbrainz.org/artist/%s#_' % trackData['artist']['mbid'])
            if artistData['artist']['type'] == "band" and\
                    (artisturi, RDF.type, MusicOntology.MusicArtist) in self.graph:
                self.graph.remove((artisturi, RDF.type, MusicOntology.MusicArtist))
                self.graph.add((artisturi, RDF.type, MusicOntology.MusicGroup))

        #now the location data!
        if 'hometown' not in artistData.keys():
            self.save()
            return

        if "http" in artistData['hometown']['value']:
            townuri = URIRef(artistData['hometown']['value'].encode('utf-8'))
            if (townuri, RDF.type, dbpediaowl.Place) not in self.graph:
                self.graph.add((townuri, RDF.type, dbpediaowl.Place))
                if "hometownName" in artistData.keys():
                    self.graph.add((townuri, foaf.name, Literal(artistData['hometownName']['value'].encode('utf-8'))))
                if "coordinates" in artistData.keys():
                    self.graph.add((townuri, geo.geometry, Literal(artistData['coordinates']['value'].encode('utf-8'))))
            self.graph.add((artisturi, dbpediaowl.hometown, townuri))
        else:
            self.graph.add((artisturi, dbpediaowl.hometown, Literal(artistData['hometown']['value'])))

        self.save()

    def artist_is_in(self, uri):
        return (URIRef(uri), RDF.type, MusicOntology.MusicArtist) in self.graph or (URIRef(uri), RDF.type, MusicOntology.MusicGroup) in self.graph


#In these functions, we need to work out the cases which have more than one result. For now, I consider the first hit!

def bandBio(name):
    sparql.setQuery("""
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

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results['results']['bindings'] == []:
        return None
    else:
        results = results['results']['bindings'][0]
        results['artist']['type'] = 'band'
    return results


def artistBio(name):
    sparql.setQuery("""
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

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results['results']['bindings'] == []:
        results = bandBio(name)
        return results

    results = results['results']['bindings'][0]
    results['artist']['type'] = 'artist'
    return results

if __name__ == "__main__":
    logging.basicConfig()
    s = Store()
    files = glob("../data/rock/trackInfo/*.json")

    artists = []
    for f in files:
        track = json.load(file(f))
        try:
            artists.append(track['track']['artist']['name'])
        except:
            pass
    artists = unique(artists)
    artistInfo = {}

    for artist in artists:
        print artist
        artistInfo[artist] = artistBio(artist)
    
    pickle.dump(artistInfo, file("../artistInfo.pickle", "w"))

    artistInfo = pickle.load(file("../artistInfo.pickle"))

    for f in files:
        track = json.load(file(f))
        if 'track' not in track.keys(): 
            #this means last.fm does not have info for this track
            continue

        trackMBID = basename(f)[:-5]
        print f

        if track['track']['artist']['name'].strip() == '': continue

        artistData = artistInfo[track['track']['artist']['name']]
        if artistData == None: continue

        s.addArtistBio(trackMBID, artistData, track['track'])
