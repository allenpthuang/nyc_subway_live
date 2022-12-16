import requests
import zipcodes
from station_table import station_table_by_line, station_table_by_zip
from transistor_config import API_SERVER

# URL_LINE = API_SERVER + '/systems/nycsubway/routes/{}'
# URL_ZIP = API_SERVER + '/systems/nycsubway/stops?latitude={}&longitude={}'
URL_LINE = API_SERVER + '/systems/us-ny-subway/routes/{}'
URL_ZIP = API_SERVER + '/systems/us-ny-subway/stops?latitude={}&longitude={}'

def stations_by_line(line):
    url = URL_LINE.format(line)
    r = requests.get(url)
    if r.status_code == 404:
        return f"Can't find {line} Line in the database!\n"

    data = r.json()
    stations = data['serviceMaps'][0]['stops']
    line_name = data['longName']

    return station_table_by_line(stations, line, line_name)



def stations_by_zip(zipcode):
    try:
        z = zipcodes.matching(zipcode)
    except:
        return f'Failed to match {zipcode}!\n'

    if len(z) == 0:
            return f'Failed to match {zipcode}!\n'

    lat = z[0]['lat']
    lon = z[0]['long']
    url = URL_ZIP.format(lat, lon)

    r = requests.post(url)
    stations = r.json()

    if len(stations) == 0:
        return f'No stations found around {zipcode}!\n'

    return station_table_by_zip(stations, zipcode)
