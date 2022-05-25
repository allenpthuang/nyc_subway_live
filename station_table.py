import colored
from colored import stylize
from pyfiglet import figlet_format
from bullet_colors import bullet_colors

def get_lens(stations):
    id_len = 0
    name_len = 0
    for s in stations:
        id_len = max(id_len, len(s['id']))
        name_len = max(name_len, len(s['name']))
    return id_len, name_len


def station_table_by_line(stations, line):
    banner = figlet_format(line + ' Line', font='starwars')
    banner = stylize(banner, colored.fg(bullet_colors[line]))
    table, border = station_table(stations)
    return border + banner + table
    

def station_table_by_zip(stations, zip_code):
    banner = figlet_format(zip_code, font='starwars')
    table, border = station_table(stations)
    return border + banner + table


def station_table(stations):
    result = ''
    entry = '│  {}  │  {}  │' + '\n'
    id_len, name_len = get_lens(stations)
    
    for s in stations:
        sid = f'{s["id"]:<{id_len + 2}}'
        sname = f'{s["name"]:<{name_len + 2}}'
        result += entry.format(sid, sname)

    header = entry.format(f'{"ID":<{id_len + 2}}',
                          f'{"Name":<{name_len + 2}}')
    width = id_len + name_len + 4 + 11
    border = '─' * width + '\n'
    result = border + header + border + result + border
    return result, border
