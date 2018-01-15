from wit import Wit
import pyowm
import json

with open('city.list.json') as data_file:
    data = json.load(data_file)

access_token = '3N5Z4M2LNX4WD3NSW62GFTBR7M3SAXLQ'
api_key = 'bc6871d0ece638528df279d5afe250ef'

client = Wit(access_token = access_token)
owm = pyowm.OWM(api_key)

def wit_response(message_text):
    resp = client.message(message_text)
    print('resp, ', resp)
    entity = None
    location = None
    try:
        entity = list(resp['entities'])[1]
        location = resp['entities']['location'][0]['value']
    except:
        pass
    return location

def pass_city_data(cityname):
    cityid = None
    for city in data:
        if (city['name'] == cityname):
            cityid = city['id']
            return cityid

def get_weather_data(cityid):
    weather = None
    print("cityid: ", cityid)
    if (type(cityid) != int):
        weather = "Invalid data!"
    else:
        observation = owm.weather_at_id(cityid)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')
        weather = "Current temperature " + str(temp['temp'])
    return weather

def determine_response(message):
    location = wit_response(message)
    id = pass_city_data(location)
    result = get_weather_data(id)
    print(result)
    return result
