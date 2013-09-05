__author__ = 'mpetyx'

from django.http import HttpResponse
from rdflib import Graph


def test(request):
    testrdf = '''
     @prefix dc: <http://purl.org/dc/terms/> .
     <http://example.org/about>
         dc:title "Someone's Homepage"@en .
     '''

    g = Graph().parse(data=testrdf, format='n3')

    print(g.serialize(format='json-ld', indent=4))


def map(request):
    latitude = request.GET.get("latitude", "")
    longitude = request.GET.get("longitude", "")

    mapGraph = '''
     @prefix dc: <http://purl.org/dc/terms/> .
     <http://example.org/about>
         dc:title "Someone's Homepage"@en .
     '''

    g = Graph().parse(data=mapGraph, format='n3')

    return HttpResponse(g.serialize(format='json-ld', indent=4), status=200)