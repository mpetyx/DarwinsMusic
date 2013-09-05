__author__ = 'mpetyx'

import pickle
import os
from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF

mbid = "6cc0ab41-adb5-457f-b90f-3e0992f7b5ff"

MUSIC = Namespace('http://eswc.com#')

storefn = os.path.expanduser('/Users/mpetyx/Desktop/projects/repos/TooLate/lastFm/tracks.n3')
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
        self.graph.add((trackuri, MUSIC.has_playcount, Literal(track.get_playcount())))
        self.graph.add((trackuri, MUSIC.has_listener_count, Literal(track.get_listener_count())))
        for tag in track.get_tags():
            self.graph.add((trackuri, MUSIC.has_tag, Literal(tag)))

        self.save()

    def track_is_in(self, uri):
        return (URIRef(uri), RDF.type, MUSIC['Track']) in self.graph


if __name__ == "__main__":

    s = Store()
    file_with_mbids = open("list_of_mbid.txt","r")
    mbids = file_with_mbids.readlines()

    for mbid in mbids:
        mbid = mbid.replace("\n","")
        track = pickle.load(file("../data/" + mbid + ".pickle", "r"))
        trackuri = URIRef('http://musicbrainz.org/recording/%s' % mbid)
        if s.track_is_in(trackuri):
            print "it already exist!"
        else:
            s.track(mbid=mbid, track=track)
            print "i saved a new one!"