__author__ = 'mpetyx'


import json

class Points:

    def __init__(self):


        json_file = open("pointsToCountry.json","r").read()
        self.myjson = json.loads(json_file)

    def CountryCode(self, ena, duo):

        return self.myjson[ena][duo]



example = Points()

print example.CountryCode("32.7574","-97.3332")