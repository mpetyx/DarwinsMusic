from rdflib import Literal, Namespace, URIRef, ConjunctiveGraph, RDF

MusicOntology = Namespace('http://purl.org/ontology/mo/')
DC = Namespace("http://purl.org/dc/terms/")
OurVocab = Namespace('http://example.org/')
foaf = Namespace("http://xmlns.com/foaf/0.1/")

storefn = abspath('../data/rock/tracks.n3')
storeuri = 'file://' + storefn

graph = ConjunctiveGraph()
graph.load(storeuri, format='n3')

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
    getAlbumInfo(glob("../data/rock/trackInfo/*.json"))

    trackFiles = glob("../data/rock/trackInfo/*.json")
    albumFiles = glob("../data/rock/albumInfo/*.json")
    addAlbumTriples(trackFiles, albumFiles)
    graph.serialize(storeuri, format='n3')
