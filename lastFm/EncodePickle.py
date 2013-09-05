__author__ = 'mpetyx'

import pickle
import datetime, os, sys, re, time
from rdflib import Graph, Literal, Namespace, URIRef, ConjunctiveGraph

mbid = "6cc0ab41-adb5-457f-b90f-3e0992f7b5ff"

track = pickle.load(file("../data/"+mbid+".pickle", "r"))

# print track.get_playcount()
# print track.get_listener_count()
# print track.get_top_tags()


MUSIC = Namespace('http://eswc.com#')

storefn = os.path.expanduser('/Users/mpetyx/Desktop/projects/repos/TooLate/lastFm/tracks.n3')
#storefn = '/home/simon/codes/film.dev/movies.n3'
storeuri = 'file://'+storefn

class Store:
    def __init__(self):
        self.graph = ConjunctiveGraph()
        if os.path.exists(storefn):
            self.graph.load(storeuri, format='n3')
        self.graph.bind('MUSIC', MUSIC)
        self.graph.bind('rev', 'http://purl.org/stuff/rev#')

    def save(self):
        self.graph.serialize(storeuri, format='n3')

    def track(self,mbid,track):

        trackuri = URIRef('http://musicbrainz.org/recording/%s' % mbid)
        self.graph.add((trackuri, MUSIC.has_playcount, Literal(track.get_playcount())))
        self.graph.add((trackuri, MUSIC.has_listener_count, Literal(track.get_listener_count())))
        for tag in track.get_tags():

            self.graph.add((trackuri, MUSIC.has_tag, Literal(tag)))

        self.save()

s = Store()
s.track(mbid=mbid,track=track)