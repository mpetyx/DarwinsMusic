__author__ = 'mpetyx'

import json

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from rdflib import Graph

from SparqlQueries import query
from MapResponseProvider import mapJson


def test(request):
    testrdf = '''
     @prefix dc: <http://purl.org/dc/terms/> .
     <http://example.org/about>
         dc:title "Someone's Homepage"@en .
     '''

    g = Graph().parse(data=testrdf, format='n3')

    print(g.serialize(format='json-ld', indent=4))


def map(request):
    # latitude = request.GET.get("latitude", "")
    # longitude = request.GET.get("longitude", "")
    #
    # mapGraph = '''
    #  @prefix dc: <http://purl.org/dc/terms/> .
    #  <http://example.org/about>
    #      dc:title "Someone's Homepage"@en .
    #  '''
    #
    # g = Graph().parse(data=mapGraph, format='n3')
    # return HttpResponse(g.serialize(format='json-ld', indent=4), status=200)

    genre = request.GET.get("genre", "")

    response = mapJson( genre)

    return HttpResponse(response, status=200)


def sparql(request):
    #http://127.0.0.1:8000/sparql?query=SELECT%20?s%20?p%20?o%20WHERE%20{%20?s%20?p%20?o}%20LIMIT%201000
    #http://127.0.0.1:8000/sparql?query=SELECT%20(COUNT(*)%20AS%20?count)%20WHERE%20{%20?s%20?p%20?o}
    query_parameters = request.GET.get("query", "")

    if query_parameters:
        result = query(query_parameters)

        # g = Graph()
        #
        # for triple in result:
        #     g.add(triple)
        # g.serialize(format='json-ld', indent=4)
        return HttpResponse(json.dumps(result), status=200)
    else:
        return HttpResponse("You need to send a get request with parameted 'query'", status=500)


def index(request):

    return render_to_response("index.html")