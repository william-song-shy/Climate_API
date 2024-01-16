from koppen_climate import *
import mapbox_geocoding
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/place/find")
def FindPlace():
    data = request.args
    return jsonify(mapbox_geocoding.search(data["name"], data["limit"])), {
        "Access-Control-Allow-Origin": "*"
    }


@app.get("/station/find")
def FindStation():
    data = request.args
    data = search_station(query=data["name"], length=data["length"])
    return jsonify(
        [
            {
                "id": i.get_id(),
                "name": i.get_name(),
                "country": i.get_country(),
                "lat": i.get_place().latitude,
                "lon": i.get_place().longitude,
            }
            for i in data
        ]
    ), {"Access-Control-Allow-Origin": "*"}


@app.get("/station/climate")
def StationClimate():
    data = request.args
    station = Station()
    station.set_by_id(data["id"])
    data, meta = station.get_climate_data()
    climatetype = data_to_koppen(data)
    return jsonify(
        {
            "id": station.get_id(),
            "name": station.get_name(),
            "country": station.get_country(),
            "lat": station.get_place().latitude,
            "lon": station.get_place().longitude,
            "data": data,
            "koppentype": climatetype,
            "chinesetype": koppen2chinese.get(climatetype),
            "source": meta.get("source")
            + " from {} to {}".format(meta.get("start"), meta.get("end")),
        }
    ), {"Access-Control-Allow-Origin": "*"}


@app.get("/point/climate")
def PointClimate():
    data = request.args
    p = Place(data["lat"], data["lon"], 0)
    data, meta = p.get_climate_data()
    climatetype = data_to_koppen(data)
    # ns = p.get_nearby_stations()
    # nsl = list()
    # if ns:
    #     for i in ns:
    #         nsl.append(
    #             {
    #                 "id": i.get_id(),
    #                 "country": i.get_country(),
    #                 "lat": i.get_place().get_lat(),
    #                 "lon": i.get_place().get_lon(),
    #                 "name": i.get_name(),
    #             }
    #         )
    return jsonify(
        {
            "country": p.get_country(),
            "nearby_stations": [],
            "data": data,
            "koppentype": climatetype,
            "chinesetype": koppen2chinese.get(climatetype),
            "source": meta.get("source")
            + " from {} to {}".format(meta.get("start"), meta.get("end")),
        }
    ), {"Access-Control-Allow-Origin": "*"}
