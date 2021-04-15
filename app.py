from apiflask import APIFlask,Schema,input, output
from apiflask.fields import String,Integer
from apiflask.validators import Length,Range
from koppen_climate import *

app = APIFlask(__name__)

class StationOut (Schema):
    id=String()
    name=String()
    country=String()



class StationFindIn (Schema):
    name = String (required=True,validate=Length(1,75))
    length=Integer(required=False,missing=10,validate=Range(2,15))

@app.get('/')
def main ():
    return {"about":"See /redoc to see how to use this API"}

@app.get('/station/find')
@input(StationFindIn,location="query")
@output(StationOut(many=True))
def FindStation(data):
    data=search_station(query=data['name'],length=data['length'])
    l=list()
    for i in data:
        l.append(
            {
                'id':i.get_id(),
                'name':i.get_name(),
                'country':i.get_country()
            })
    return l
