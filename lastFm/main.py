__author__ = 'mpetyx'

# http://andreatlai.com/2013/01/17/last-fm-via-python/

import pulast
import pylast
import pickle

API_KEY = 'f1a01dc19e25cfa39158d9c72695fdda'
API_SECRET = 'd45dcf1b6c1921a7157297a299fb5e5a'

"""things that enable using the API"""
#authenticate
username = 'petmiker'
password_hash = pylast.md5('toolate')

#generate network key
network = pylast.get_lastfm_network(
    api_key=API_KEY, api_secret=API_SECRET,
    username=username, password_hash=password_hash)


def getTrackInfo(mbid):
    track = network.get_track_by_mbid(mbid)
    #check whether it returned info/ track is empty
    pickle.dump(track, file("../data/"+mbid+".pickle", "w"))


if __name__ == "__main__":
    getTrackInfo(mbid="6cc0ab41-adb5-457f-b90f-3e0992f7b5ff")


#open a file to write to
# out_file = open("output.csv", "wt")

#get data about Taylor Swift
#artist = network.get_artist('Michael Jackson')


#musicbrainz_artist_id = artist.get_mbid()

#print musicbrainz_artist_id
#albums = ['Bad']


#for every item in the list of albums (in this case "Red" only),
#get the track listing.
#for i in albums:
#    i = network.get_album(artist, i)
#    tracks = i.get_tracks()
    #for every track in tracklisting, return it's length
    #(in seconds) and playcount (in Last.fm total "scrobbles")


#    for track in tracks:

        # print "the playcount count is:"
        # print track.get_playcount()
        #
        # print "the listener count is:"
        # print track.get_listener_count()
        #
        # print "the tags are"
        # print track.get_tags()


        #comma-delimited, write data to file
#         out_file.write(str(track))
#         out_file.write(', %s' % str(tracklen))
#         out_file.write(', %s' % str(playcount))
#         out_file.write('\n')
#
# out_file.close()