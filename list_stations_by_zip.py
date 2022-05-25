import requests
import zipcodes
from station_table import station_table_by_zip

URL = 'https://demo.transiter.dev/systems/nycsubway/stops?latitude={}&longitude={}'

def stations_by_zip(zipcode):
	try:
		z = zipcodes.matching(zipcode)
	except:
		return f'Failed to match {zipcode}!\n'

	if len(z) == 0:
            return f'Failed to match {zipcode}!\n'

	lat = z[0]['lat']
	lon = z[0]['long']
	url = URL.format(lat, lon)

	r = requests.post(url)
	stations = r.json()

	if len(stations) == 0:
		return f'No stations found around {zipcode}!\n'

	return station_table_by_zip(stations, zipcode)
