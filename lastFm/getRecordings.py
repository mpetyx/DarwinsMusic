__author__ = 'gopalkoduri'

import lxml
from uuid import uuid1
import json
from urllib2 import urlopen

tag = "jazz"
pageLimit = 50
pages = 100

for page in xrange(pages):
	data = urlopen("http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag="+tag+"&page="+str(page)+"&limit="+str(pageLimit)+"&api_key=9d8eec456625c74e02a7e23bd1d7c68a&format=json").read()
	data = json.loads(data)
	for track in data['toptracks']['track']:
		if track['mbid'] == '':
			mbid = "_"+str(uuid1())
		else:
			mbid = track['mbid']
		print mbid
		json.dump(track, file("../data/"+tag+"/"+mbid+".json", 'w'))
