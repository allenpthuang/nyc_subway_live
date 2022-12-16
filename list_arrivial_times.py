import requests
import colored
import textwrap
from pyfiglet import figlet_format
from colored import stylize
from datetime import datetime, timedelta
from bullet_colors import bullet_colors
from transistor_config import API_SERVER
from collections import defaultdict

SHOW_TOP_K = 16
# URL = API_SERVER + '/systems/nycsubway/stops/{}'
URL = API_SERVER + '/systems/us-ny-subway/stops/{}'

def list_arrivial_times(station):
    url = URL.format(station)
    r = requests.get(url)

    if r.status_code == 404:
        err_msg = (
                f'Station {station} does not seem to exist!\n'
                f'Try use the following to find Station IDs:\n'
                f'    curl sbwy.live/<line>\n'
                f'    curl sbwy.live/R    # list all stops along R train\n'
                )
        return err_msg

    data = r.json()
    
    result = ''

    dict_dir = {}

    PER_HEADSIGN_K = SHOW_TOP_K // 2
    headsign_count = defaultdict(lambda: 0)
    for s in data['stopTimes']:
        if sum(headsign_count.values()) > SHOW_TOP_K + 1:
            break

        if headsign_count[s['headsign']] >= PER_HEADSIGN_K:
            continue

        headsign_count[s['headsign']] += 1
        try:
            arr_time = datetime.fromtimestamp(int(s['arrival']['time']))
        except:
            arr_time = datetime.fromtimestamp(int(s['departure']['time']))

        delta = arr_time - datetime.now()
        if - delta > timedelta(seconds=60) or delta >= timedelta(minutes=60):
            continue

        delta = delta // timedelta(minutes=1)
        if delta <= 0:
            delta_str = stylize(f'{"ARR":>9}', colored.attr('blink'))
        else:
            delta_str = str(delta)
        
        route = s['trip']['route']['id']

        try:
            bullet_color = bullet_colors[route]
        except KeyError:
            bullet_color = 'white'
        
        arr_str = (
                f'{stylize("⬤ ", colored.fg(bullet_color))} {route:<4}'
                + f'{delta_str:>9}'
        )


        try:
            dict_dir[s['headsign']].append(arr_str)
        except KeyError:
            dict_dir[s['headsign']] = []
            dict_dir[s['headsign']].append(arr_str)


    n_dir = len(dict_dir.keys())
    n_entries = 0
    for arr in dict_dir.values():
        n_entries = max(n_entries, len(arr))

    line = '│' + '   {}   │' * n_dir + '\n'

    for i in range(0, n_entries):
        arr_strs = []
        for _, arr in dict_dir.items():
            try:
                arr_strs.append(arr[i])
            except:
                arr_strs.append(f'{"":<16}')


        result += line.format(*arr_strs)

    width = len(line) - 1 + (16 - 2) * n_dir
    border = '─' * width + '\n'
    result = border + result + border

    headers = []
    for k in dict_dir.keys():
        headers.append(textwrap.wrap(k, 20))

    header_height = 0
    for h in headers:
        header_height = max(header_height, len(h))

    for idx, item in enumerate(headers):
        if len(item) < header_height:
            headers[idx] = [' '] * (header_height - len(item)) + item

    header = '│' + ' {} │' * n_dir + '\n'
    for i in range(0, header_height):
        header_strs = []
        for h in headers:
            header_strs.append('{0:<20}'.format(h[header_height - i - 1]))
        result = header.format(*header_strs) + result

    banner = figlet_format(data['name'], font='smslant')
    result = border + banner + border + result
    result = border + 'Station: ' + data['name'] + '\n' + result

    return result

