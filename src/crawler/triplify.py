from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF
from os.path import basename, abspath, exists
from glob import glob
import json
import sys

MusicOntology = Namespace('http://purl.org/ontology/mo/')
foaf = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/terms/")
OurVocab = Namespace('http://example.org/')
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
dbpediaowl = Namespace("http://dbpedia.org/ontology/")

#TODO: Add owl:sameAs between MB and DBPedia when there is an mbid for artist from last.fm
#Also add influence relations

class Store:
    def __init__(self, tripleFile):
        self.graph = ConjunctiveGraph()
        self.storefn = abspath(tripleFile)
        self.storeuri = 'file://' + self.storefn
        if exists(self.storefn):
            self.graph.load(self.storeuri, format='n3')

        self.graph.bind('mo', MusicOntology)
        self.graph.bind('ourvocab', OurVocab)
        self.graph.bind('dc', DC)
        self.graph.bind('foaf', foaf)
        self.graph.bind('geo', geo)
        self.graph.bind('dbpediaowl', dbpediaowl)
        self.graph.bind('rev', 'http://purl.org/stuff/rev#')

    def save(self):
        self.graph.serialize(self.storeuri, format='n3')

    def addTrack(self, mbid, track):
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

        if isinstance(track['toptags'], dict) and 'tag' in track['toptags'].keys():
            for tag in track['toptags']['tag']:
                if isinstance(tag, dict):
                    self.graph.add((trackuri, OurVocab.has_tag, Literal(tag['name'])))

    def addArtist(self, trackMBID, artistData, trackData):
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

    def _matchAlbum(self, trackInfo, albumFiles):
        """
        A function to return the correct match of an album given a track.
        Deprecated for most cases where the match is done using mbids.
        Use only for cases where there is no mbid link betweeb album and track.
        """
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

    def addAlbum(self, trackMBID, albumInfo):
        """
        A function to add album data into triple store. At the moment, only the releasedate is taken
        from the album data. More to be added soon.
        """
        try:
            albumInfo = albumInfo['album']
        except:
            return

        if 'releasedate' not in albumInfo.keys():
            return

        trackuri = URIRef('http://musicbrainz.org/recording/%s#_' % trackMBID)
        self.graph.add((trackuri, OurVocab.has_releasedate, Literal(albumInfo['releasedate'].strip().encode('utf-8'))))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Not enough arguments:\n\nUsage: python <script.py> <tag> <dataFolder>\n\n"
        exit()

    #track triples
    tag = sys.argv[1]
    dataFolder = sys.argv[2]

    s = Store(dataFolder + '/' + tag + '/triples.nt')

    files = glob(dataFolder + '/' + tag + '/trackInfo/*.json')
    albumFiles = glob(dataFolder + '/' + tag + '/albumInfo/*.json')

    for f in files:
        trackInfo = json.load(file(f))
        if not (isinstance(trackInfo, dict) and 'track' in trackInfo.keys()):
            #this means last.fm does not have info for this track
            continue
        mbid = basename(f)[:-5]
        print mbid
        trackuri = URIRef('http://musicbrainz.org/recording/%s#_' % mbid)

        #the store automatically takes care of duplicates as graph is a 'set' of triples
        s.addTrack(mbid=mbid, track=trackInfo['track'])

        #artist triples
        artistMBID = None
        try:
            artistMBID = trackInfo['track']['artist']['mbid']
        except:
            artistMBID = str(uuid5(NAMESPACE_URL, trackInfo['track']['artist']['url']))

        if artistMBID:
            artistData = json.load(file(dataFolder + '/artistInfo/' + artistMBID + '.json'))
            if artistData:
                s.addArtist(trackMBID=mbid, artistData=artistData, trackData=trackInfo['track'])

        #album triples
        albumInfo = None
        if 'album' in trackInfo['track'].keys():
            if 'mbid' not in trackInfo['track']['album'].keys() or trackInfo['track']['album']['mbid'] == '':
                try:
                    albumMBID = str(uuid5(NAMESPACE_URL, trackInfo['track']['album']['url'].encode('utf-8')))
                    if exists(dataFolder + '/' + tag + '/albumInfo/' + albumMBID + '.json'):
                        albumInfo = json.load(file(dataFolder + '/' + tag + '/albumInfo/' + albumMBID + '.json'))
                except:
                    af = s._matchAlbum(trackInfo['track'], albumFiles)
                    if af:
                        albumInfo = json.load(file(af))
            else:
                if exists(dataFolder + '/' + tag + '/albumInfo/' + trackInfo['track']['album']['mbid'] + '.json'):
                    albumInfo = json.load(file(dataFolder + '/' + tag + '/albumInfo/' + trackInfo['track']['album']['mbid'] + '.json'))
        if albumInfo:
            s.addAlbum(trackMBID=mbid, albumInfo=albumInfo)

    s.save()
