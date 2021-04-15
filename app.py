from apiflask import APIFlask,Schema,input, output
from apiflask.fields import String,Integer,Float
from apiflask.validators import Length,Range
from koppen_climate import *

app = APIFlask(__name__)

class StationOut (Schema):
    id=String()
    name=String()
    country=String()
    lat=Float()
    lon=Float()



class StationFindIn (Schema):
    name = String (required=True,validate=Length(1,75))
    length=Integer(required=False,missing=10,validate=Range(2,15))

@app.get('/')
def main ():
    """Show some imformation

    """
    return {"about":"See /redoc to see how to use this API"}

@app.get('/station/find')
@input(StationFindIn,location="query")
@output(StationOut(many=True))
def FindStation(data):
    """Find a station by name

    the meteostat will return 400 if the name is too short to search<br>
    this API will return the id(in meteostat),name,country(ISO 3166-1 alpha-2) and latlon data
    """
    data=search_station(query=data['name'],length=data['length'])
    l=list()
    for i in data:
        l.append(
            {
                'id':i.get_id(),
                'name':i.get_name(),
                'country':i.get_country(),
                'lat':i.get_place().get_lat(),
                'lon':i.get_place().get_lon()
            })
    return l
