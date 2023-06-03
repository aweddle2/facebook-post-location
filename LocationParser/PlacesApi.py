# May replace this with the entire Python Library, but for now it's just one API call
import requests
from LocationParser.Config import Config

def ResolvePlaceName(text):
    waffle = Config()
    apiKey = waffle.Config['GoogleApi']['PlacesApiKey']

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+text+"%20Australia&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="+apiKey

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

