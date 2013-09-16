#!/usr/bin/env python

from os.path import basename, exists, abspath
from uuid import uuid5, NAMESPACE_URL
from urllib2 import urlopen, quote
from bs4 import BeautifulSoup
from time import sleep
from time import time
import json

class lastFm:
    """
    This class has all the necessary functions to get full information of top recordings
    given a tag in last.fm, which includes the album information as well. The number of 
    recordings is determined by other class parameters like pageOffset, pageLimit and numPages.
    """
    def __init__(self, key, tag, dataFolder, numPages = 10, pageLimit = 50, pageOffset = 0, delay = 1):
        self.key = key
        self.tag = tag
        self.pageOffset = pageOffset
        self.pageLimit = pageLimit
        self.numPages = numPages
        self.dataFolder = dataFolder
        self.delay = delay
        self.lastRequest = time()

    def wait(self):
        actualDelay = time() - self.lastRequest
        if actualDelay < self.delay: sleep(actualDelay)
        self.lastRequest = time()
    
    def _getComments(self, url):
        wait()

        data = urlopen(url).read()
        soup = BeautifulSoup(data)

        res = soup.find_all('li', 'message')
        comments = []
        for i in res:
            comments.append(i.p.text.strip())

        return comments

    def storeTopRecs(self):
        """
        This function gets the top recordings of the genre. The number of recordings is
        determined by other class parameters like pageOffset, pageLimit and numPages.
        """
        print "Getting top recordings of ", self.tag, " tag"
        for page in xrange(self.pageOffset, self.pageOffset+self.numPages):
            data = urlopen("http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag=" + \
                    self.tag + "&page=" + str(page) + "&limit=" + str(self.pageLimit) + \
                    "&api_key=" + self.key + "&format=json").read()
            data = json.loads(data)
            for track in data['toptracks']['track']:
                if track['mbid'] == '':
                    mbid = str(uuid5(NAMESPACE_URL, track['url'].encode('utf-8')))
                else:
                    mbid = track['mbid']
                print mbid
                json.dump(track, file(self.dataFolder + self.tag + "/toptracks/" + mbid + ".json", 'w'))

            wait()

        
    def storeRecInfo(self, topTrackFile):
        track = json.load(file(topTrackFile))
        mbid = basename(f)[:-5]
        if exists(self.dataFolder + self.tag + "/trackInfo/" + mbid + ".json"): return

        print "Track: ", mbid
        if track['mbid'] == '':
            try:
                url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + self.key + "&artist="\
					    + quote(track['artist']['name'].encode('utf-8')) + \
                        "&track=" + quote(track["name"].encode('utf-8')) + "&format=json"
            except:
                print "No mbid and artist info. Skipping"
                return
        else:
            url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + self.key + "&mbid="\
					+ track['mbid'] + "&format=json"

        wait()

        trackInfo = urlopen(url).read()
        trackInfo = json.loads(trackInfo)
        if 'track' not in trackInfo.keys():
            return

        try:
            comments = self._getComments(trackInfo['url'])
            trackInfo['comments'] = comments
        except:
            pass
        json.dump(trackInfo, file(self.dataFolder + self.tag + "/trackInfo/" + mbid + ".json", 'w'))

    def storeAlbumInfo(self, trackFile):
        track = json.load(file(trackFile))
        try:
            track = track['track']
        except:
            return
        if 'album' not in track.keys():
            print "No album info for the track. Skipping."
            return

        mbid = track['album']['mbid']
        if mbid == '':
            mbid = str(uuid5(NAMESPACE_URL, track['album']['url'].encode('utf-8')))
            try:
                url = "http://ws.audioscrobbler.com/2.0/?method=album.getInfo&api_key=" + self.key + "&artist="\
                        + quote(track['artist']['name'].encode('utf-8')) + "&album=" + \
                        quote(track['album']['name'].encode('utf-8')) + "&format=json"
            except:
                print "No artist/album info to bring full album info. Skipping."
                return
        else:
            url = "http://ws.audioscrobbler.com/2.0/?method=album.getInfo&api_key=" + self.key + "&mbid="\
                    + mbid + "&format=json"

        if exists(dataFolder + self.tag + "/albumInfo/" + mbid + ".json"): return

        wait()

        print "Album: ", mbid
        albumInfo = urlopen(url).read()
        albumInfo = json.loads(albumInfo)
        json.dump(albumInfo, file(dataFolder + self.tag + "/albumInfo/" + mbid + ".json", "w"))

