import pyowm

__author__ = 'watchara.p'


class Weather(object):
    def __init__(self):
        pass
    def __repr__(self):
        return "Hell, world"

    def load_weather(self):
        owm = pyowm.OWM('2edaae5381cd2151829c57a93d13a9f1')
        # owm.weather_at_coords(-22.57, -43.12,1)
        observation = owm.weather_at_coords(12.675205, 101.135644)
        # observation = owm.weather_at_place('Rayong')
        w = observation.get_weather()
        self.weather = w
        self.wind = w.get_wind()  # {'speed': 4.6, 'deg': 330}
        self.RH = w.get_humidity()/100  # 87
        self.temp = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

