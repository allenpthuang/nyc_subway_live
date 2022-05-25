import json
import requests
import colored
import textwrap
from pyfiglet import figlet_format
from colored import stylize
from datetime import datetime, timedelta
from bullet_colors import bullet_colors

SHOW_TOP_K = 16
URL = 'https://demo.transiter.dev/systems/nycsubway/stops/{}'

def get_station(station):
    u = URL.format(station)
    r = requests.get(u)

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

    for s in data['stop_times'][:SHOW_TOP_K]:
        try:
            arr_time = datetime.fromtimestamp(s['arrival']['time'])
        except:
            arr_time = datetime.fromtimestamp(s['departure']['time'])

        delta = arr_time - datetime.now()
        if - delta > timedelta(seconds=60) or delta >= timedelta(minutes=60):
            continue

        delta = delta // timedelta(minutes=1)
        if delta <= 0:
            delta_str = stylize(f'{"ARR":>9}', colored.attr('blink'))
        else:
            delta_str = str(delta)
        
        route = s['trip']['route']['id']
        arr_str_old = (
              s['trip']['route']['id']
              + ' Train arriving in '
              + str(delta)
              + ' at '
              + arr_time.strftime('%Y-%m-%d %H:%M:%S')
        )

        try:
            bullet_color = bullet_colors[route]
        except KeyError:
            bullet_color = 'white'
        
        arr_str = (
                f'{stylize("⬤ ", colored.fg(bullet_color))} {route:<4}'
                + f'{delta_str:>9}'
        )


        try:
            dict_dir[s['direction']].append(arr_str)
        except KeyError:
            dict_dir[s['direction']] = []
            dict_dir[s['direction']].append(arr_str)


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

    result = border + result

    banner = figlet_format(data['name'], font='smslant')

    result = border + banner + result
    
    result = border + 'Station: ' + data['name'] + '\n' + result

    return result

