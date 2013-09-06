__author__ = 'mpetyx'

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import re


def mapJson(request):
    sparql = SPARQLWrapper("http://192.168.2.27:8080/openrdf-sesame/repositories/Music")

    superQuery = """

    PREFIX geo-pos:<http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX umbel-ac:<http://umbel.org/umbel/ac/>
    PREFIX sw-vocab:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
    PREFIX ff:<http://factforge.net/>
    PREFIX music-ont:<http://purl.org/ontology/mo/>
    PREFIX dc-term:<http://purl.org/dc/terms/>
    PREFIX om:<http://www.ontotext.com/owlim/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX pext:<http://proton.semanticweb.org/protonext#>
    PREFIX dc:<http://purl.org/dc/elements/1.1/>
    PREFIX onto:<http://www.ontotext.com/>
    PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX yago:<http://mpii.de/yago/resource/>
    PREFIX xml:<http://www.w3.org/XML/1998/namespace>
    PREFIX umbel:<http://umbel.org/umbel#>
    PREFIX pkm:<http://proton.semanticweb.org/protonkm#>
    PREFIX wordnet16:<http://xmlns.com/wordnet/1.6/>
    PREFIX owl:<http://www.w3.org/2002/07/owl#>
    PREFIX dbpediaowl:<http://dbpedia.org/ontology/>
    PREFIX wordn-sc:<http://www.w3.org/2006/03/wn/wn20/schema/>
    PREFIX nytimes:<http://data.nytimes.com/>
    PREFIX dbp-prop:<http://dbpedia.org/property/>
    PREFIX geonames:<http://sws.geonames.org/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbpedia:<http://dbpedia.org/resource/>
    PREFIX oasis:<http://psi.oasis-open.org/iso/639/#>
    PREFIX geo-ont:<http://www.geonames.org/ontology#>
    PREFIX umbel-en:<http://umbel.org/umbel/ne/wikipedia/>
    PREFIX mo:<http://purl.org/ontology/mo/>
    PREFIX bbc-pont:<http://purl.org/ontology/po/>
    PREFIX lingvoj:<http://www.lingvoj.org/ontology#>
    PREFIX ourvocab:<http://example.org/>
    PREFIX psys:<http://proton.semanticweb.org/protonsys#>
    PREFIX umbel-sc:<http://umbel.org/umbel/sc/>
    PREFIX dbp-ont:<http://dbpedia.org/ontology/>

    SELECT DISTINCT ?s ?title ?listeners ?hits ?performer ?point ?date
    FROM <file://C:/fakepath/tracks.n3>
    WHERE {
    ?s a mo:Track.
    ?s dc-term:title ?title.
    ?s ourvocab:has_listener_count ?listeners.
    ?s ourvocab:has_playcount ?hits.
    ?s ourvocab:has_releasedate ?date.

    ?s mo:performer ?pid.

    ?pid foaf:name ?performer.

    ?pid dbp-ont:hometown ?hid.
    ?hid geo:geometry ?point.

    }
    LIMIT 10000
    """

    countQuery  = """
    SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o}
    """

    sparql.setQuery(superQuery)

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()


    res = results["results"]["bindings"]

    # hits = []
    # listeners = []
    # performers = []
    # titles = []
    # points = []
    dates = []

    for result in res:
        year = result['date']['value']

        temp = re.findall(r'\d{4}', year)
        if temp:
            year = temp[0]
            year = year[:-1]+'0'
            dates.append(year)

    distinct_years = list(set(dates))

    hits = {}
    listeners = {}
    performers = []
    points = []

    for year in distinct_years:
        hits["%s"%year] = []

    for year in distinct_years:
        listeners["%s"%year] = []

    for result in res:

        year = result['date']['value']

        res = re.findall(r'\d{4}', year)

        if res:
            year = res[0]
            year = year[:-1]+'0'
            # dates.append(year)

            belongs_to_that_decade = False

            lem = result['point']['value'].replace("POINT(", "")
            lem = lem.replace(")", "")

            ena, duo = lem.split(" ")
            points.append([duo, ena])
            performers.append(result['performer']['value'])

            for decade in distinct_years:
                if year == decade:

                    hits["%s"%decade].append(result['hits']['value'])
                    listeners["%s"%decade].append(result['listeners']['value'])

                    # titles.append(result['title']['value'])
                else:
                    hits["%s"%decade].append(0)
                    listeners["%s"%decade].append(0)

        else:
            continue



    finalized_json = {}

    finalized_json['names'] = performers
    finalized_json['hits'] = hits
    finalized_json['viewers'] = listeners
    # finalized_json['titles'] = titles
    finalized_json['coords'] = points
    finalized_json['dates'] = distinct_years

    return json.dumps(finalized_json)