#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib2 import urlopen
from glob import glob
from time import time, sleep
import json
import sys

lastRequest = time()
delay = 1

def getComments(url):
    global lastRequest
    global delay
    actualDelay = time() - lastRequest
    if actualDelay < delay: sleep(actualDelay)
    lastRequest = time()

    data = urlopen(url).read()
    soup = BeautifulSoup(data)

    res = soup.find_all('li', 'message')
    comments = []
    for i in res:
        comments.append(i.p.text.strip())

    return comments

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Not enough arguments:\n\nUsage: python <script.py> <tag> <dataFolder>\n\n"
        exit()

    tag = sys.argv[1]
    dataFolder = sys.argv[2]
    
    files = glob(dataFolder + tag + '/trackInfo/*.json')
    for f in files:
        trackInfo = json.load(file(f))
        try:
            trackInfo = trackInfo['track']
        except:
            continue

        print f
        comments = getComments(trackInfo['url'])
        trackInfo['comments'] = comments
        json.dump(trackInfo, file(f, 'w'))
