__author__ = "gopalkoduri"

import json
from urllib2 import urlopen, quote
from glob import glob
from os.path import basename, exists
from time import sleep

tag = 'rock'
files = glob("../data/rock/toptracks/*.json")

for f in files:
    track = json.load(file(f))
    if track['mbid'] == '':
        mbid = basename(f)[:-5]
        print mbid, track['artist']['name'], track['name']
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=9d8eec456625c74e02a7e23bd1d7c68a&artist=" + quote(track['artist']['name'].encode('utf-8')) + "&track=" + quote(track["name"].encode('utf-8')) + "&format=json"
    else:
        mbid = track['mbid']
        url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=9d8eec456625c74e02a7e23bd1d7c68a&mbid=" + track['mbid'] + "&format=json"
    if exists("../data/" + mbid + ".json"): continue

    print mbid
    trackInfo = urlopen(url).read()
    trackInfo = json.loads(trackInfo)
    json.dump(trackInfo, file("../data/" + tag + "/trackInfo/" + mbid + ".json", 'w'))
    sleep(0.25)
