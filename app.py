from apiflask import APIFlask, Schema, input, output
from apiflask.fields import String, Integer, Float, Dict, List
from apiflask.validators import Length, Range
from koppen_climate import *
import mapbox_geocoding

app = APIFlask(__name__)


@app.error_processor
def my_error_handler(status_code, message, detail, headers):
    return {
        'status_code': status_code,
        'message': message,
        'detail': detail
    }, status_code, {'Access-Control-Allow-Origin': '*'}


class StationOut(Schema):
    id = String()
    name = String()
    country = String()
    lat = Float()
    lon = Float()


class StationFindIn(Schema):
    name = String(required=True, validate=Length(1, 75))
    length = Integer(required=False, missing=10, validate=Range(2, 15))


class StationIn(Schema):
    id = String(required=True)


class PlaceIn (Schema):
    name = String(required=True, validate=Length(1, 80))
    limit = Integer(required=False, missing=5, validate=Range(1, 15))


class PlaceOut (Schema):
    zh_name = String()
    en_name = String()
    lat = Float()
    lon = Float()
    bbox = List(Float())


class StationandClimateOut(Schema):
    id = String()
    name = String()
    country = String()
    lat = Float()
    lon = Float()
    data = List(Dict())
    koppentype = String()
    chinesetype = String()
    source = String()


class PointIn(Schema):
    lat = Float(required=True, validate=Range(-90, 90))
    lon = Float(required=True, validate=Range(-180, 180))


class PointandClimateOut(Schema):
    country = String()
    nearby_stations = List(Dict())
    data = List(Dict())
    koppentype = String()
    chinesetype = String()
    source = String()


@app.get('/')
def main():
    """Show some imformation

    """
    return {"about": "See /redoc to see how to use this API"}


@app.get("/place/find")
@input(PlaceIn, location="query")
@output(PlaceOut(many=True))
def FindPlace(data):
    """Find a place
    Find a place (city,country,village etc.) by the name given.
    This API returns and accepts the name both in Chinese and English
    """
    return mapbox_geocoding.search(data['name'], data['limit']), {'Access-Control-Allow-Origin': '*'}


@app.get('/station/find')
@input(StationFindIn, location="query")
@output(StationOut(many=True))
def FindStation(data):
    """Find a station by name

    the meteostat will return 400 if the name is too short to search<br>
    this API will return the id(in meteostat),name,country(ISO 3166-1 alpha-2) and latlon data
    """
    data = search_station(query=data['name'], length=data['length'])
    l = list()
    for i in data:
        l.append(
            {
                'id': i.get_id(),
                'name': i.get_name(),
                'country': i.get_country(),
                'lat': i.get_place().get_lat(),
                'lon': i.get_place().get_lon()
            })
    return l, {'Access-Control-Allow-Origin': '*'}


@app.get('/station/climate')
@input(StationIn, location="query")
@output(StationandClimateOut)
def StationClimate(data):
    """Get the climate data

    """
    station = Station()
    station.set_by_id(data['id'])
    data=station.get_climate_data()
    climatetype = data.get_koppen()
    koppen2chinese = {
        'Af': "热带雨林",
        'Am': "热带季风",
        'Aw': "热带草原",
        'As': "热带草原",
        'BWk': "温带干旱",
        'BWh': "热带沙漠",
        'BSh': "热带半干旱",
        'BSk': "温带半干旱",
        'Csa': "地中海",
        'Csb': "地中海",
        'Csc': "地中海",
        'Cfa': "亚热带湿润",
        'Cwa': "亚热带湿润",
        'Cwb': "温带海洋",
        'Cfb': "温带海洋",
        'Cfc': "温带海洋",
        'Dsa': "温带大陆",
        'Dsb': "温带大陆",
        'Dsc': "亚寒带",
        'Dsd': "亚寒带",
        'Dwa': "温带大陆性湿润",
        'Dwb': "温带大陆性湿润",
        'Dwc': "亚寒带",
        'Dwd': "亚寒带",
        'Dfa': "温带大陆性湿润",
        'Dfb': "温带大陆性湿润",
        'Dfc': "亚寒带",
        'Dfd': "亚寒带",
        'ET': "苔原",
        'EF': "冰原"
    }
    return {
        'id': station.get_id(),
        'name': station.get_name(),
        'country': station.get_country(),
        'lat': station.get_place().get_lat(),
        'lon': station.get_place().get_lon(),
        'data': data.get_data(),
        'koppentype': climatetype,
        'chinesetype': koppen2chinese.get(climatetype),
        'source': data.get_meta().get('source')
    }, {'Access-Control-Allow-Origin': '*'}


@app.get('/point/climate')
@input(PointIn, location="query")
@output(PointandClimateOut)
def PointClimate(data):
    p = Place(data['lat'], data['lon'], 0)
    data=p.get_climate_data()
    climatetype =data.get_koppen()
    koppen2chinese = {
        'Af': "热带雨林",
        'Am': "热带季风",
        'Aw': "热带草原",
        'As': "热带草原",
        'BWk': "温带干旱",
        'BWh': "热带沙漠",
        'BSh': "热带半干旱",
        'BSk': "温带半干旱",
        'Csa': "地中海",
        'Csb': "地中海",
        'Csc': "地中海",
        'Cfa': "亚热带湿润",
        'Cwa': "亚热带湿润",
        'Cwb': "温带海洋",
        'Cfb': "温带海洋",
        'Cfc': "温带海洋",
        'Dsa': "温带大陆",
        'Dsb': "温带大陆",
        'Dsc': "亚寒带",
        'Dsd': "亚寒带",
        'Dwa': "温带大陆性湿润",
        'Dwb': "温带大陆性湿润",
        'Dwc': "亚寒带",
        'Dwd': "亚寒带",
        'Dfa': "温带大陆性湿润",
        'Dfb': "温带大陆性湿润",
        'Dfc': "亚寒带",
        'Dfd': "亚寒带",
        'ET': "苔原",
        'EF': "冰原"
    }
    ns = p.get_nearby_stations()
    nsl = list()
    if ns:
        for i in ns:
            nsl.append({'id': i.get_id(), 'country': i.get_country(), 'lat': i.get_place().get_lat(),
                        'lon': i.get_place().get_lon(), 'name': i.get_name()})
    return {
        'country': p.get_country(),
        'nearby_stations': nsl,
        'data': data.get_data(),
        'koppentype': climatetype,
        'chinesetype': koppen2chinese.get(climatetype),
        'source': data.get_meta().get('source')
    }, {'Access-Control-Allow-Origin': '*'}
