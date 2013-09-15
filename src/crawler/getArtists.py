from os.path import exists
from glob import glob
from os import mkdir
import json
import sys

sys.path.append('dbpedia')
from dbpedia import dbpedia

class artist:
    """
    This class has all the methods necessary to get and store the artist data from 
    DBPedia, given the dataFolder and tag.
    """
    def __init__(self, tag, dataFolder):
        self.trackFiles = glob(dataFolder + tag + "/trackInfo/" + "*.json")
        self.artists = {}
        self._getUniqArtists()
        if not exists(dataFolder + "/artistInfo/"):
            mkdir(dataFolder + "/artistInfo/")
        self.dbpedia = dbpedia()

    def _getUniqArtists(self):
        for f in self.trackFiles:
            track = json.load(file(f))
            try:
                mbid = track['track']['artist']['mbid']
                if mbid == '':
                    mbid = "_"+str(uuid5(NAMESPACE_URL, track['track']['artist']['url']))
                self.artists[mbid] = track['track']['artist']['name']
            except:
                pass

    def storeArtistInfo(self):
        for mbid, artist in self.artists.items():
            if exists(dataFolder + '/artistInfo/' + mbid + ".json"):
                continue
            print artist
            artistInfo = self.dbpedia.getArtist(artist)
            json.dump(artistInfo, file(dataFolder + '/artistInfo/' + mbid + ".json", "w"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Not enough arguments:\n\nUsage: python <script.py> <tag> <dataFolder>\n\n"
        exit()

    tag = sys.argv[1]
    dataFolder = sys.argv[2]
    a = artist(tag, dataFolder)
    a.storeArtistInfo()

