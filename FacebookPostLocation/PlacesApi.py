# May replace this with the entire Python Library, but for now it's just one API call
import requests
import json
from FacebookPostLocation.Config import Config


def ResolvePlaceName(text):
    conf = Config()
    apiKey = conf.Config['GoogleApi']['PlacesApiKey']

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+text + \
        "%20Australia&inputtype=textquery&fields=formatted_address%2Cname%2Cgeometry&key="+apiKey

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return GooglePlacesResponse.from_json(json.loads(response.text))


class GooglePlacesResponse:
    def __init__(self, formatted_address, lat, lng, name):
        self.formatted_address = formatted_address
        self.lat = lat
        self.lng = lng
        self.name = name

    def __iter__(self):
        yield from {
            "formatted_address": self.formatted_address,
            "lat": self.lat,
            "lng": self.lng,
            "name": self.name
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        if (len(json_dct['candidates']) == 0):
            return None
        # TODO error checking needed here.
        return GooglePlacesResponse(json_dct['candidates'][0]['formatted_address'],
                                    json_dct['candidates'][0]['geometry']['location']['lat'],
                                    json_dct['candidates'][0]['geometry']['location']['lng'],
                                    json_dct['candidates'][0]['name']
                                    )
