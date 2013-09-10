from urllib2 import urlopen


def getCountry(lat, lng):
    url = "http://ws.geonames.org/countryCode?lng=" + str(lng) + "&lat=" + str(lat)
    country = urlopen(url).read().strip()
	if len(country) != 2:
		return "Unknown"
    return country

