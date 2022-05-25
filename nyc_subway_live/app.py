import falcon
import falcon.asgi
from list_arrivial_times import list_arrivial_times
from list_stations import stations_by_line, stations_by_zip

class Station:
    async def on_get(self, rep, resp, query):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        if len(query) == 1:
            resp.text = stations_by_line(query)
        elif len(query) == 5 and query.isnumeric():
            resp.text = stations_by_zip(query)
        else:
            resp.text = list_arrivial_times(query)

class HelpMsg:
    async def on_get(self, rep, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = (
            'Usage:\n'
            '    curl sbwy.live               # show this help message\n'
            '    curl sbwy.live/R             # show all R train stations\n'
            '    curl sbwy.live/11232         # show all stations near the area with zip code = 11232\n'
            '    curl sbwy.live/<station_id>  # show the train arrival timetable at the staion\n'
            )

app = falcon.asgi.App()
station = Station()
help_msg = HelpMsg()
app.add_route('/', help_msg)
app.add_route('/{query}', station)
