from glob import glob
import json

def uniqArtists():
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
    return artists

def storeArtistInfo():
    artists = uniqArtists()
    artistInfo = {}

    for artist in artists:
        print artist
        artistInfo[artist] = artistBio(artist)
    
    pickle.dump(artistInfo, file("../data/rock/artistInfo.pickle", "w"))

    artistInfo = pickle.load(file("../data/rock/artistInfo.pickle"))

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
