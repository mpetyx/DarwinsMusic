__author__ = 'mpetyx'


import json

class Points:

    def __init__(self,file_name):

        if file_name is None:

            file_name = "pointsToCountry.json"

        json_file = open(file_name,"r").read()
        self.myjson = json.loads(json_file)

    def CountryCode(self, ena, duo):

        return self.myjson[ena][duo]



# example = Points()
#
# print example.CountryCode("32.7574","-97.3332")