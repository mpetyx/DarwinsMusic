__author__ = 'mpetyx'

from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF
import json
from os.path import basename, abspath
from glob import glob

MusicOntology = Namespace('http://purl.org/ontology/mo/')
DC = Namespace("http://purl.org/dc/terms/")
OurVocab = Namespace('http://example.org/')
foaf = Namespace("http://xmlns.com/foaf/0.1/")

storefn = abspath('../tracks.n3')
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
        self.graph.bind('rev', 'http://purl.org/stuff/rev#')

    def save(self):
        self.graph.serialize(storeuri, format='n3')

    def track(self, mbid, track):
        trackuri = URIRef('http://musicbrainz.org/recording/%s#_' % mbid)
        self.graph.add((trackuri, RDF.type, MusicOntology.Track))
        self.graph.add((trackuri, DC.title, Literal(track['name'])))
        self.graph.add((trackuri, OurVocab.has_playcount, Literal(track['playcount'])))
        self.graph.add((trackuri, OurVocab.has_listener_count, Literal(track['listeners'])))

        if track['artist']['mbid'] != '':
            artisturi = URIRef('http://musicbrainz.org/artist/%s#_' % track['artist']['mbid'])
            self.graph.add((artisturi, RDF.type, MusicOntology.MusicArtist))
            self.graph.add((trackuri, MusicOntology.performer, artisturi))
            self.graph.add((artisturi, foaf.name, Literal(track['artist']['name'])))

        for tag in track['toptags']['tag']:
            self.graph.add((trackuri, OurVocab.has_tag, Literal(tag['name'])))

        self.save()

    def track_is_in(self, uri):
        return (URIRef(uri), RDF.type, MusicOntology['track']) in self.graph


if __name__ == "__main__":
    s = Store()
    files = glob("../data/*.json")

    for f in files:
        track = json.load(file(f))
        if 'track' not in track.keys(): 
            #this means last.fm does not have info for this track
            continue
        mbid = basename(f)[:-5]
        trackuri = URIRef('http://musicbrainz.org/recording/%s#_' % mbid)
        if s.track_is_in(trackuri):
            print "it already exist!"
        else:
            s.track(mbid=mbid, track=track['track'])
            print "i saved a new one!"
