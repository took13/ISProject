import requests
import json
__author__ = 'watchara.p'

class Weather(object):
    def __init__(self, city_name, ladtitude, longitude):
        self.city_name = city_name
        self.lad = ladtitude
        self.lon = longitude
        self.load_weather()

        self.temp = self.temp
        self.wind_speed = self.wind_speed
        self.wind_deg = self.wind_deg
        # self.load_weather(city_name)

    def __repr__(self):
        return "<Weather at {} temp {} wind speed {} wind direction {}".format(self.city_name, self.temp, self.wind_speed, self.wind_deg)

    def load_weather(self):
        api_url = "http://api.openweathermap.org/data/2.5/weather"
        app_id = "2edaae5381cd2151829c57a93d13a9f1"
        request = requests.get(url=api_url, params=dict(q=self.city_name, APPID=app_id, units='metric',lat=self.lad, lon=self.lon ))
        wind_data = json.loads(request.content)

        # try:
        self.temp = wind_data['main']['temp']
        self.wind_speed = wind_data['wind']['speed']
        self.wind_deg = wind_data['wind']['deg']

        # except:
        # print("Error")
        # print('speed:' + str(wspeed))
        # print('degree:' + str(wdeg))
        # print('temp:' + str(wtemp))
        # print(wdata)

    def save_to_mongo(self):
        pass

    def json(self):
        pass