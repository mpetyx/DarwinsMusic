__author__ = 'mpetyx'

import json

from geoToCountry import getCountry

json_file = open("query.json","r").read()
myjson = json.loads(json_file)

results =  myjson['results']['bindings']

custom_result = {}

for res in results:
    # print res['point']['value']
    lem = res['point']['value'].replace("POINT(", "")
    lem = lem.replace(")", "")

    ena, duo = lem.split(" ")
    # points.append([duo, ena])
    myCountry = getCountry(duo, ena)

    custom_result[duo]={ena: myCountry}

    # print custom_result

dumpData = open("pointsToCountry.json", "w")
dumpData.write(json.dumps(custom_result))