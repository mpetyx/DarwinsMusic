from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF
from os.path import basename, abspath, exists
from glob import glob
import json

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
		self.storeuri = 'file://' + storefn
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

        for tag in track['toptags']['tag']:
            self.graph.add((trackuri, OurVocab.has_tag, Literal(tag['name'])))

        #self.save()

    def isTrackIn(self, uri):
        return (URIRef(uri), RDF.type, MusicOntology['track']) in self.graph

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

    def isArtistIn(self, uri):
        return (URIRef(uri), RDF.type, MusicOntology.MusicArtist) in self.graph or (URIRef(uri), RDF.type, MusicOntology.MusicGroup) in self.graph

    def _matchAlbum(trackInfo, albumFiles):
        """
        A function to return the correct match of an album given a track.
        """
        #TODO: Deprecated, effect the new mbid based match
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



if __name__ == "__main__":
    s = Store()
    files = glob("../data/rock/trackInfo/*.json")

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


    getAlbumInfo(glob("../data/rock/trackInfo/*.json"))

    trackFiles = glob("../data/rock/trackInfo/*.json")
    albumFiles = glob("../data/rock/albumInfo/*.json")
    addAlbumTriples(trackFiles, albumFiles)
    graph.serialize(storeuri, format='n3')

    s.addArtistBio(trackMBID, artistData, track['track'])

	s.save()
