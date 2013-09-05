__author__ = 'mpetyx'

import pickle
import os
from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF
import json
from os.path import basename

mbid = "6cc0ab41-adb5-457f-b90f-3e0992f7b5ff"

MUSIC = Namespace('http://eswc.com#')

storefn = os.path.expanduser('../tracks.n3')
storeuri = 'file://' + storefn


class Store:
    def __init__(self):
        self.graph = ConjunctiveGraph()
        if os.path.exists(storefn):
            self.graph.load(storeuri, format='n3')
        self.graph.bind('MUSIC', MUSIC)
        self.graph.bind('rev', 'http://purl.org/stuff/rev#')

    def save(self):
        self.graph.serialize(storeuri, format='n3')

    def track(self, mbid, track):
        trackuri = URIRef('http://musicbrainz.org/recording/%s' % mbid)
        self.graph.add((trackuri, RDF.type, MUSIC['Track']))
        self.graph.add((trackuri, MUSIC.has_playcount, Literal(track['playcount'])))
        self.graph.add((trackuri, MUSIC.has_listener_count, Literal(track['listeners'])))
		for tag in data['track']['toptags']['tag']:
            self.graph.add((trackuri, MUSIC.has_tag, Literal(tag['name'])))

        self.save()

    def track_is_in(self, uri):
        return (URIRef(uri), RDF.type, MUSIC['Track']) in self.graph


if __name__ == "__main__":

    s = Store()
    files = glob("../data/*.json")

    for f in files:
        track = json.load(file(f))
		mbid = basename(f)[:-5]
        trackuri = URIRef('http://musicbrainz.org/recording/%s' % mbid)
        if s.track_is_in(trackuri):
            print "it already exist!"
        else:
            s.track(mbid=mbid, track=track['track'])
            print "i saved a new one!"
