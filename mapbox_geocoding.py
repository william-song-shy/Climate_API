import requests
endpoint = "https://api.mapbox.com/geocoding/v5/mapbox.places/"


def search(query, limits=5):
    params = {
        "types": "place",
        "language": "zh-Hans,en",
        "worldview": "cn",
        "limit": limits,
        "access_token": "pk.eyJ1Ijoic29uZ2hvbmd5aSIsImEiOiJja25jdDdjZG4xM25iMnVvb2NjbDl3YjMwIn0.PJZgJQmBgR_g-vsSD7uKFA"
    }
    url = endpoint+query+".json"
    r = requests.get(url, params=params)
    r = r.json()
    res = [{
        'zh_name': i.get('place_name_zh-Hans'),
        'en_name': i.get('place_name_en'),
        'bbox': i.get('bbox'),
        'lat': i.get('center')[1],
        'lon': i.get('center')[0]
    } for i in r.get('features')]
    return res


if __name__ == "__main__":
    print(search("贝尼迈拉勒"))
