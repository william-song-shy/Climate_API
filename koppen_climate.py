import numpy as np
import requests
import mapbox_geocoding

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


def data_to_koppen(data: dict):
    avgtemp = list()
    precip = list()
    for i in data:
        avgtemp.append(i["tavg"])
        precip.append(i["prcp"])
    avgtemp = np.array(avgtemp)
    precip = np.array(precip)
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


class Place:
    """
    A class of a place/point
    """

    def __init__(self, latitude, longitude, elevation):
        """
        Init the class
        :param latitude: the latitude of the place
        :param longitude: the longitude of the place
        :param elevation: the elevation of the place
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def get_climate_data(self):
        """
        A function to get the climate data
        :return: the climate data in ClimateData class
        """
        r = get_to_json(
            "https://api.meteostat.net/v2/point/climate",
            params={
                "lat": self.latitude,
                "lon": self.longitude,
                "alt": self.elevation,
            },
        )
        data = r["data"]
        meta = r["meta"]
        return data, meta

    def get_nearby_stations(self):
        """The function to get nearby stations
        :return: the list of nearby stations in Station class
        """
        data = get_to_json(
            "https://api.meteostat.net/v2/stations/nearby",
            params={"lat": self.latitude, "lon": self.longitude},
        )["data"]
        ans = list()
        if not data:
            return None
        for i in data:
            id = i["id"]
            temp = Station()
            temp.set_by_id(id)
            ans.append(temp)
        return ans

    def get_country(self):
        """
        Get the country of the place
        :return: Alpha-2 code of the country (ISO 3166)
        """
        data = mapbox_geocoding.reverse(lat=self.latitude, lon=self.longitude)
        if data is None:
            return None
        data = data.get("context")[-1]
        return data.get("short_code")


class Station:
    def __init__(self):
        pass

    def set_by_data(self, data):
        """
        Set the station with data
        :param data: the data
        :return: noting
        """
        self.__id = data["id"]
        self.__name = data["name"].get("en")
        self.__country = data["country"]
        self.__place = Place(
            float(data["latitude"]), float(data["longitude"]), int(data["elevation"])
        )  # 经度纬度海拔

    def set_by_id(self, ida):
        """
        Set the station by meteostat id
        :param ida: meteostat id
        :return: noting
        """
        data = get_to_json(
            "https://api.meteostat.net/v2/stations/meta?id={}".format(ida)
        )["data"]
        self.set_by_data(data)

    def get_climate_data(self):
        """
        Get the climate data
        :return: the climate data in ClimateData class
        """
        data = get_to_json(
            "https://api.meteostat.net/v2/stations/climate",
            params={"station": self.__id},
        )
        if not data["data"]:
            return self.__place.get_climate_data()
        return data["data"], data["meta"]

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_country(self):
        return self.__country

    def get_place(self):
        return self.__place


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
    ans = list()
    for i in data:
        temp = Station()
        temp.set_by_data(i)
        ans.append(temp)
    return ans
