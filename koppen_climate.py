import numpy as np
import requests


def get_to_json(url, params={}):
    """
    A function to get a url which return a json and decode it into dict
    :param url: The url use to get
    :param params: params
    :return: the json response in dict
    """
    return requests.get(url, headers={"x-api-key": "cEghsfXW7CG5W43dEzrvhjn3a8mZjkYm"}, params=params).json()


class ClimateData:
    """A class of climate data
    """
    def __init__(self, data):
        """
        A function to init the class
        :param data:the data of the climate
        """
        self.__data = data

    def get_koppen(self):
        """Get the climate type

        :return: the köppen type of the climate(i.e. Cfa,Af .etc).
        """
        data = self.__data
        avgtemp = list()
        precip = list()
        for i in data:
            avgtemp.append(i['tavg'])
            precip.append(i['prcp'])
        avgtemp = np.array(avgtemp)
        precip = np.array(precip)
        totalprecip = sum(precip)
        climate = ""
        if min(avgtemp) >= 18.0:
            # Tropical Rainforest
            if min(precip) >= 60.0:
                climate = 'Af'
                return climate
            # Tropical Monsoon
            elif min(precip) < 60.0 and (min(precip) / totalprecip) > 0.04:
                climate = 'Am'
                return climate
            else:
                # Tropical Savanna Dry Summer
                if np.where(precip == min(precip))[0][0] >= 6 and np.where(precip == min(precip))[0][0] <= 8:
                    climate = 'As'
                    return climate
                # Tropical Savanna Dry Winter
                else:
                    climate = 'Aw'
                    return climate

        # Group B (Arid and Semiarid)
        aridity = np.mean(avgtemp) * 20.0
        warmprecip = sum(precip[3:9])
        coolprecip = sum(precip[0:3]) + sum(precip[9:12])
        if warmprecip / totalprecip >= 0.70:
            aridity = aridity + 280.0
        elif warmprecip / totalprecip >= 0.30 and warmprecip / totalprecip < 0.70:
            aridity = aridity + 140.0
        else:
            aridity = aridity + 0.0

        # Arid Desert (BW)
        if totalprecip / aridity < 0.50:
            # Hot Desert (BWh)
            if np.mean(avgtemp) > 18.0:
                climate = 'BWh'
                return climate
            # Cold Desert (BWk)
            else:
                climate = 'BWk'
                return climate

        if 'A' in climate:
            return climate

        # Semi-Arid/Steppe (BS)
        elif totalprecip / aridity >= 0.50 and totalprecip / aridity < 1.00:
            # Hot Semi-Arid (BSh)
            if np.mean(avgtemp) > 18.0:
                climate = 'BSh'
                return climate
            # Cold Semi-Arid (BSk)
            else:
                climate = 'BSk'
                return climate

        if 'B' in climate:
            return climate

        # Group C (Temperate)
        sortavgtemp = avgtemp
        sortavgtemp.sort()
        tempaboveten = np.shape(np.where(avgtemp > 10.0))[1]
        coldwarmratio = max(max(precip[0:2]), precip[11]) / min(precip[5:8])
        warmcoldratio = max(precip[5:8]) / min(min(precip[0:2]), precip[11])
        if min(avgtemp) >= 0.0 and min(avgtemp) <= 18.0 and max(avgtemp) >= 10.0:
            # Humid Subtropical (Cfa)
            if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4.0:
                climate = 'Cfa'
            # Temperate Oceanic (Cfb)
            elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4.0:
                climate = 'Cfb'
            # Subpolar Oceanic (Cfc)
            elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3:
                climate = 'Cfc'

            # Monsoon-influenced humid subtropical (Cwa)
            if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4 and warmcoldratio > 10.0:
                climate = 'Cwa'
            # Subtropical Highland/Temperate Oceanic with Dry Winter (Cwb)
            elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4 and warmcoldratio > 10.0:
                climate = 'Cwb'
            # Cold Subtropical Highland/Subpolar Oceanic with Dry Winter (Cwc)
            elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio > 10.0:
                climate = 'Cwc'

            # Hot summer Mediterranean (Csa)
            if min(avgtemp) > 0.0 and max(avgtemp) > 22.0 and tempaboveten >= 4 and \
                    coldwarmratio >= 3.0 and min(precip[5:8]) < 30.0:
                climate = 'Csa'
            # Warm summer Mediterranean (Csb)
            elif min(avgtemp) > 0.0 and max(avgtemp) < 22.0 and tempaboveten >= 4 and \
                    coldwarmratio >= 3.0 and min(precip[5:8]) < 30.0:
                climate = 'Csb'
            # Cool summer Mediterranean (Csc)
            elif min(avgtemp) > 0.0 and tempaboveten >= 1 and tempaboveten <= 3 and \
                    coldwarmratio >= 3.0 and min(precip[5:8]) < 30.0:
                climate = 'Csc'

            if 'C' in climate:
                return climate

        # Group D (Continental)
        if min(avgtemp) < 0.0 and max(avgtemp) > 10.0:
            # Hot summer humid continental (Dfa)
            if max(avgtemp) > 22.0 and tempaboveten >= 4:
                climate = 'Dfa'
            # Warm summer humid continental (Dfb)
            elif max(avgtemp) < 22.0 and tempaboveten >= 4:
                climate = 'Dfb'
            # Subarctic (Dfc)
            elif tempaboveten >= 1 and tempaboveten <= 3:
                climate = 'Dfc'
            # Extremely cold subarctic (Dfd)
            elif min(avgtemp) < -38.0 and tempaboveten >= 1 and tempaboveten <= 3:
                climate = 'Dfd'

            # Monsoon-influenced hot humid continental (Dwa)
            if max(avgtemp) > 22.0 and tempaboveten >= 4 and warmcoldratio >= 10:
                climate = 'Dwa'
            # Monsoon-influenced warm humid continental (Dwb)
            elif max(avgtemp) < 22.0 and tempaboveten >= 4 and warmcoldratio >= 10:
                climate = 'Dwb'
            # Monsoon-influenced subarctic (Dwc)
            elif tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio >= 10:
                climate = 'Dwc'
            # Monsoon-influenced extremely cold subarctic (Dwd)
            elif min(avgtemp) < -38.0 and tempaboveten >= 1 and tempaboveten <= 3 and warmcoldratio >= 10:
                climate = 'Dwd'

            # Hot, dry continental (Dsa)
            if max(avgtemp) > 22.0 and tempaboveten >= 4 and coldwarmratio >= 3 and min(precip[5:8]) < 30.0:
                climate = 'Dsa'
            # Warm, dry continental (Dsb)
            elif max(avgtemp) < 22.0 and tempaboveten >= 4 and coldwarmratio >= 3 and min(precip[5:8]) < 30.0:
                climate = 'Dsb'
            # Dry, subarctic (Dsc)
            elif tempaboveten >= 1 and tempaboveten <= 3 and coldwarmratio >= 1 and coldwarmratio >= 3 and \
                    min(precip[5:8]) < 30.0:
                climate = 'Dsc'
            # Extremely cold, dry subarctic (Dsd)
            elif min(avgtemp) < -38.0 and tempaboveten >= 1 and tempaboveten <= 3 and coldwarmratio >= 3 and \
                    min(precip[5:8]) < 30.0:
                climate = 'Dsd'

            if 'D' in climate:
                return climate

        # Group E (Polar and alpine)
        if max(avgtemp) < 10.0:
            # Tundra (ET)
            if max(avgtemp) > 0.0:
                climate = 'ET'
            # Ice cap (EF)
            else:
                climate = 'EF'

    def get_data(self):
        """
        Get the data
        :return: the data
        """
        return self.__data


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
        self.__latitude = latitude
        self.__longitude = longitude
        self.__elevation = elevation

    def get_climate_data(self):  # 千万不要对Station导出的Place执行这个操作
        """
        A function to get the climate data
        :return: the climate data in ClimateData class
        """
        data = get_to_json("https://api.meteostat.net/v2/point/climate", params=
        {"lat": self.__latitude, "lon": self.__longitude, "alt": self.__elevation})['data']
        return ClimateData(data)

    def get_nearby_stations(self):
        """The function to get nearby stations
        :return: the list of nearby stations in Station class
        """
        data = get_to_json("https://api.meteostat.net/v2/stations/nearby",
                           params={"lat": self.__latitude, "lon": self.__longitude})['data']
        ans = list()
        if not data:
            return None
        for i in data:
            id = i['id']
            temp = Station()
            temp.set_by_id(id)
            ans.append(temp)
        return ans

    def get_country(self):
        data = requests.get(
            "https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zom=18&addressdetails=1".format(
                self.__latitude, self.__longitude
            )
        ).json()
        if data.get('error'):
            return None
        return data.get('address').get('country_code')

    def __repr__(self):
        return "({},{},{})".format(self.__latitude, self.__longitude, self.__elevation)

    def get_lat(self):
        return self.__latitude

    def get_lon(self):
        return self.__longitude

    def get_ele(self):
        return self.__elevation


class Station:
    def __init__(self):
        pass

    def set_by_data(self, data):
        self.__id = data['id']
        self.__name = data['name'].get('en')
        self.__country = data['country']
        self.__place = Place(float(data["latitude"]), float(data["longitude"]), int(data["elevation"]))  # 经度纬度海拔

    def set_by_id(self, ida):
        data = get_to_json("https://api.meteostat.net/v2/stations/meta?id={}".format(ida))['data']
        self.set_by_data(data)

    def get_climate_data(self):
        data = get_to_json("https://api.meteostat.net/v2/stations/climate", params={"station": self.__id})
        return ClimateData(data['data'])

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_country(self):
        return self.__country

    def get_place(self):
        return self.__place


def search_station(query, length=10):
    data = get_to_json("https://api.meteostat.net/v2/stations/search",
                       params={"query": query, 'limit': length})['data']
    ans = list()
    for i in data:
        temp = Station()
        temp.set_by_data(i)
        ans.append(temp)
    return ans
