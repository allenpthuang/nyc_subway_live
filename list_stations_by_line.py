import json
from station_table import station_table_by_line

with open('stops.json', 'r') as f:
    data = json.load(f)


def stations_by_line(line):
    stations = [s for s in data if s['id'][:1] == line]
    stations = [s for s in stations
                    if s['id'][-1] != 'N' and s['id'][-1] != 'S']

    if len(stations) == 0:
        return f"Can't find {line} Line in the database!\n"

    return station_table_by_line(stations, line)


