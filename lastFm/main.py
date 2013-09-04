__author__ = 'mpetyx'

# http://andreatlai.com/2013/01/17/last-fm-via-python/

import pylast

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

#open a file to write to
out_file = open("output.csv", "wt")

#get data about Taylor Swift
artist = network.get_artist('Michael Jackson')
albums = ['Bad']

#for every item in the list of albums (in this case "Red" only),
#get the track listing.
for i in albums:
    i = network.get_album(artist, i)
    tracks = i.get_tracks()
    print tracks
    #for every track in tracklisting, return it's length
    #(in seconds) and playcount (in Last.fm total "scrobbles")
    for track in tracks:
        tracklen = track.get_duration() / 1000
        playcount = track.get_playcount()
        print playcount

        #comma-delimited, write data to file
        out_file.write(str(track))
        out_file.write(', %s' % str(tracklen))
        out_file.write(', %s' % str(playcount))
        out_file.write('\n')

out_file.close()