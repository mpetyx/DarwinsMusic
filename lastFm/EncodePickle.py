__author__ = 'mpetyx'

import pickle
from rdflib import Graph, Literal, Namespace, URIRef, ConjunctiveGraph

mbid = "6cc0ab41-adb5-457f-b90f-3e0992f7b5ff"

track = pickle.load(file("../data/"+mbid+".pickle", "r"))

# print track.get_playcount()
# print track.get_listener_count()
# print track.get_top_tags()

g = ConjunctiveGraph()

MUSIC = Namespace('http://eswc.com#')

trackuri = URIRef('http://musicbrainz.org/recording/%s' % mbid)

g.add((trackuri, MUSIC.has_playcount, Literal(track.get_playcount())))

g.add((trackuri, MUSIC.has_listener_count, Literal(track.get_listener_count())))

for tag in track.get_tags():

    g.add((trackuri, MUSIC.has_tag, Literal(tag)))


print g.serialize(format='n3')2