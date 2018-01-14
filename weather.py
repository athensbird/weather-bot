import pyowm
import requests
api_key = 'bc6871d0ece638528df279d5afe250ef'

def getWeather(location):
    r = requests.get("https://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=bc6871d0ece638528df279d5afe250ef")
    print(r.content)

print(getWeather('Manhattan, KS'))
