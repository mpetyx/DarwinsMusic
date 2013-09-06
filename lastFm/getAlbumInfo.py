__author__ = "gopalkoduri"

import json
from urllib2 import urlopen, quote
from glob import glob
from os.path import basename, exists, abspath
from time import sleep
from uuid import uuid1

from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF
from glob import glob

MusicOntology = Namespace('http://purl.org/ontology/mo/')
DC = Namespace("http://purl.org/dc/terms/")
OurVocab = Namespace('http://example.org/')
foaf = Namespace("http://xmlns.com/foaf/0.1/")

storefn = abspath('../data/rock/tracks.n3')
storeuri = 'file://' + storefn

graph = ConjunctiveGraph()
graph.load(storeuri, format='n3')

def getProperAlbum(trackInfo, albumFiles):
    try:
        albumName = trackInfo['album']['name']
        artistName = trackInfo['artist']['name']
    except:
        return None

    for af in albumFiles:
        albumInfo = json.load(file(af))
        albumInfo = albumInfo['album']
        if albumName == albumInfo['name'] and artistName == albumInfo['artist']:
            return af

def addAlbumTriples(trackFiles, albumFiles):
    for tf in trackFiles:
        trackInfo = json.load(file(tf))
        try:
            trackInfo = trackInfo['track']
        except:
            continue
        if 'album' in trackInfo.keys():
            if 'mbid' not in trackInfo['album'].keys() or trackInfo['album']['mbid'] == '':
                af = getProperAlbum(trackInfo, albumFiles)
                if af == None:
                    continue
            else:
                af = '../data/rock/albumInfo/'+trackInfo['album']['mbid']+'.json'
            print af
            #create triples
            albumInfo = json.load(file(af))
            try:
                albumInfo = albumInfo['album']
            except:
                Gcontinue
            if 'releasedate' not in albumInfo.keys():
                continue

            trackMBID = basename(tf)[:-5]
            trackuri = URIRef('http://musicbrainz.org/recording/%s#_' % trackMBID)

            graph.add((trackuri, OurVocab.has_releasedate, Literal(albumInfo['releasedate'].encode('utf-8'))))

def getAlbumInfo(files):
    for f in files:
        track = json.load(file(f))
        try:
            track = track['track']
        except:
            continue
        if 'album' not in track.keys():
            print "No album info."
            continue
        mbid = track['album']['mbid']
        if mbid == '':
            mbid = "_"+str(uuid1())
            try:
                url = "http://ws.audioscrobbler.com/2.0/?method=album.getInfo&api_key=9d8eec456625c74e02a7e23bd1d7c68a&artist=" + quote(track['artist']['name'].encode('utf-8')) + "&album=" + quote(track['album']['name'].encode('utf-8')) + "&format=json"
            except:
                print "No artist/album info"
                continue
        else:
            url = "http://ws.audioscrobbler.com/2.0/?method=album.getInfo&api_key=9d8eec456625c74e02a7e23bd1d7c68a&mbid=" + mbid + "&format=json"
        if exists("../data/rock/albumInfo/" + mbid + ".json"): continue

        albumInfo = urlopen(url).read()
        albumInfo = json.loads(albumInfo)
        json.dump(albumInfo, file("../data/rock/albumInfo/" + mbid + ".json", 'w'))
        sleep(0.25)

if __name__ == "__main__":
    getAlbumInfo(glob("../data/rock/trackInfo/*.json"))

    trackFiles = glob("../data/rock/trackInfo/*.json")
    albumFiles = glob("../data/rock/albumInfo/*.json")
    addAlbumTriples(trackFiles, albumFiles)
    graph.serialize(storeuri, format='n3')
