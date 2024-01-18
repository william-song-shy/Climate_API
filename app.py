from koppen_climate import (
    search_station,
    data_to_koppen,
    koppen2chinese,
    get_station_meta,
)
import mapbox_geocoding
from flask import Flask, jsonify, request
from meteostat import Stations, Point, Normals
import pandas as pd

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
                "id": i.get("id"),
                "name": i.get("name").get("en"),
                "country": i.get("country"),
                "lat": i.get("latitude"),
                "lon": i.get("longitude"),
            }
            for i in data
        ]
    ), {"Access-Control-Allow-Origin": "*"}


@app.get("/station/climate")
def StationClimate():
    id_ = request.args.get("id")
    data = Normals(id_, 1991, 2020)
    data = data.fetch()
    if data.empty:
        return jsonify({"error": "No data"}), {"Access-Control-Allow-Origin": "*"}
    meta = get_station_meta(id_)
    climatetype = data_to_koppen(data)
    data = data.to_dict(orient="records")
    data = [{k: None if pd.isna(v) else v for k, v in i.items()} for i in data]
    return jsonify(
        {
            "id": meta.get("id"),
            "name": meta.get("name").get("en"),
            "country": meta.get("country"),
            "lat": meta.get("latitude"),
            "lon": meta.get("longitude"),
            "data": data,
            "koppentype": climatetype,
            "chinesetype": koppen2chinese.get(climatetype),
            "source": "",
        }
    ), {"Access-Control-Allow-Origin": "*"}


@app.get("/point/climate")
def PointClimate():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    stations = Stations()
    stations = stations.nearby(lat, lon)
    stations = stations.fetch(5)
    data = Normals(Point(lat, lon), 1991, 2020)
    data = data.fetch()
    if data.empty:
        return jsonify({"error": "No data"}), {"Access-Control-Allow-Origin": "*"}
    climatetype = data_to_koppen(data)
    data = data.to_dict(orient="records")
    data = [{k: None if pd.isna(v) else v for k, v in i.items()} for i in data]
    nsl = [
        {
            "id": index,
            "name": i.get("name"),
            "country": i.get("country"),
            "lat": i.get("latitude"),
            "lon": i.get("longitude"),
        }
        for index, i in stations.iterrows()
    ]
    return jsonify(
        {
            "lat": lat,
            "lon": lon,
            "data": data,
            "koppentype": climatetype,
            "chinesetype": koppen2chinese.get(climatetype),
            "country": mapbox_geocoding.get_country(lat, lon),
            "source": "",
            "nearby_stations": nsl,
        }
    ), {"Access-Control-Allow-Origin": "*"}
