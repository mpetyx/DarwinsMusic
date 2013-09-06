__author__ = 'mpetyx'


def country(data):
    result = {}

    result['name'] = data['name']
    result['latitude'] = data['latitude']
    result['longitude'] = data['longitude']

    return result


def mapJson(request):
    result = {}

    countries = request['countries']
    list_of_countries = []

    for country in countries:
        list_of_countries.append(country(country))