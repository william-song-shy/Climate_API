import numpy as np
import requests
import mapbox_geocoding
from pandas import DataFrame

koppen2chinese = {
    "Af": "热带雨林",
    "Am": "热带季风",
    "Aw": "热带草原",
    "As": "热带草原",
    "BWk": "温带干旱",
    "BWh": "热带沙漠",
    "BSh": "热带半干旱",
    "BSk": "温带半干旱",
    "Csa": "地中海",
    "Csb": "地中海",
    "Csc": "地中海",
    "Cfa": "亚热带湿润",
    "Cwa": "亚热带湿润",
    "Cwb": "温带海洋",
    "Cfb": "温带海洋",
    "Cfc": "温带海洋",
    "Dsa": "温带大陆",
    "Dsb": "温带大陆",
    "Dsc": "亚寒带",
    "Dsd": "亚寒带",
    "Dwa": "温带大陆性湿润",
    "Dwb": "温带大陆性湿润",
    "Dwc": "亚寒带",
    "Dwd": "亚寒带",
    "Dfa": "温带大陆性湿润",
    "Dfb": "温带大陆性湿润",
    "Dfc": "亚寒带",
    "Dfd": "亚寒带",
    "ET": "苔原",
    "EF": "冰原",
}


def get_to_json(url, params={}):
    """
    A function to get a url which return a json and decode it into dict
    :param url: The url use to get
    :param params: params
    :return: the json response in dict
    """
    r = requests.get(
        url, headers={"x-api-key": "cEghsfXW7CG5W43dEzrvhjn3a8mZjkYm"}, params=params
    )
    if r.status_code != 200:
        raise Exception("return status" + str(r.status_code))
    else:
        return r.json()


def data_to_koppen(data: DataFrame):
    avgtemp = np.array(data["tavg"].tolist())
    precip = np.array(data["prcp"].tolist())
    totalprecip = sum(precip)
    if min(avgtemp) >= 18.0:
        if min(precip) >= 60.0:
            return "Af"
        # Tropical Monsoon
        elif min(precip) < 60.0 and (min(precip) / totalprecip) > 0.04:
            return "Am"
        else:
            # Tropical Savanna Dry Summer
            if (
                np.where(precip == min(precip))[0][0] >= 6
                and np.where(precip == min(precip))[0][0] <= 8
            ):
                return "As"
            else:
                return "Aw"
    aridity = np.mean(avgtemp) * 20.0
    warmprecip = sum(precip[3:9])
    if warmprecip / totalprecip >= 0.70:
        aridity = aridity + 280.0
    elif warmprecip / totalprecip >= 0.30 and warmprecip / totalprecip < 0.70:
        aridity = aridity + 140.0
    else:
        aridity = aridity + 0.0
    if totalprecip / aridity < 0.50:
        if np.mean(avgtemp) > 18.0:
            return "BWh"
        else:
            return "BWk"
    elif totalprecip / aridity >= 0.50 and totalprecip / aridity < 1.00:
        if np.mean(avgtemp) > 18.0:
            return "BSh"
        else:
            return "BSk"
    sortavgtemp = avgtemp
    sortavgtemp.sort()
    tempaboveten = np.shape(np.where(avgtemp > 10.0))[1]
    coldwarmratio = max(max(precip[0:2]), precip[11]) / min(precip[5:8])
    warmcoldratio = max(precip[5:8]) / min(min(precip[0:2]), precip[11])
    if min(avgtemp) >= 0.0 and min(avgtemp) <= 18.0 and max(avgtemp) >= 10.0:
        if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4.0:
            return "Cfa"
        elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4.0:
            return "Cfb"
        elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3:
            return "Cfc"
        if (
            min(avgtemp) > 0.0
            and max(avgtemp) > 22.0
            and tempaboveten >= 4
            and warmcoldratio > 10.0
        ):
            return "Cwa"
        elif (
            min(avgtemp) > 0.0
            and max(avgtemp) < 22.0
            and tempaboveten >= 4
            and warmcoldratio > 10.0
        ):
            return "Cwb"
        elif (
            min(avgtemp) > 0.0
            and tempaboveten >= 1
            and tempaboveten <= 3
            and warmcoldratio > 10.0
        ):
            return "Cwc"
        if (
            min(avgtemp) > 0.0
            and max(avgtemp) > 22.0
            and tempaboveten >= 4
            and coldwarmratio >= 3.0
            and min(precip[5:8]) < 30.0
        ):
            return "Csa"
        elif (
            min(avgtemp) > 0.0
            and max(avgtemp) < 22.0
            and tempaboveten >= 4
            and coldwarmratio >= 3.0
            and min(precip[5:8]) < 30.0
        ):
            return "Csb"
        elif (
            min(avgtemp) > 0.0
            and tempaboveten >= 1
            and tempaboveten <= 3
            and coldwarmratio >= 3.0
            and min(precip[5:8]) < 30.0
        ):
            return "Csc"
    if min(avgtemp) < 0.0 and max(avgtemp) > 10.0:
        if max(avgtemp) > 22.0 and tempaboveten >= 4:
            return "Dfa"
        elif max(avgtemp) < 22.0 and tempaboveten >= 4:
            return "Dfb"
        elif tempaboveten >= 1 and tempaboveten <= 3:
            return "Dfc"
        elif min(avgtemp) < -38.0 and tempaboveten >= 1 and tempaboveten <= 3:
            return "Dfd"
        if max(avgtemp) > 22.0 and tempaboveten >= 4 and warmcoldratio >= 10:
            return "Dwa"
        elif max(avgtemp) < 22.0 and tempaboveten >= 4 and warmcoldratio >= 10:
            return "Dwb"
        elif tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio >= 10:
            return "Dwc"
        elif (
            min(avgtemp) < -38.0
            and tempaboveten >= 1
            and tempaboveten <= 3
            and warmcoldratio >= 10
        ):
            return "Dwd"
        if (
            max(avgtemp) > 22.0
            and tempaboveten >= 4
            and coldwarmratio >= 3
            and min(precip[5:8]) < 30.0
        ):
            return "Dsa"
        elif (
            max(avgtemp) < 22.0
            and tempaboveten >= 4
            and coldwarmratio >= 3
            and min(precip[5:8]) < 30.0
        ):
            return "Dsb"
        elif (
            tempaboveten >= 1
            and tempaboveten <= 3
            and coldwarmratio >= 1
            and coldwarmratio >= 3
            and min(precip[5:8]) < 30.0
        ):
            return "Dsc"
        elif (
            min(avgtemp) < -38.0
            and tempaboveten >= 1
            and tempaboveten <= 3
            and coldwarmratio >= 3
            and min(precip[5:8]) < 30.0
        ):
            return "Dsd"
    if max(avgtemp) < 10.0:
        if max(avgtemp) > 0.0:
            return "ET"
        else:
            return "EF"


def search_station(query, length=10):
    """
    Search station by the name
    :param query: the name
    :param length: the length
    :return: a list of class Station
    """
    # todo : fix the bug of return 401
    data = get_to_json(
        "https://api.meteostat.net/v2/stations/search",
        params={"query": query, "limit": length},
    )["data"]
    return data

def get_station_meta (id):
    """
    Get the meta data of a station
    :param id: the id of the station
    :return: the meta data
    """
    data = get_to_json(
        "https://api.meteostat.net/v2/stations/meta",
        params={"id": id},
    )["data"]
    return data