
__author__ = 'watchara.p'

from flask import Flask, render_template, abort
import json

app = Flask(__name__)
app.secret_key = "took"
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyD1OsoG7BT3hfORu8kIjhAPNWqLtNWfFyA"
# GoogleMaps(app)

PLANTS = {
    'G1': {
        'name': 'Glow SPP1',
        'location': '10, Soi G - 2, Pakornsongkrawhrat Road, Hemaraj Eastern Industrial Estate (Map Ta Phut), Huaypong, Muang District, Rayong 21150, Thailand',
        'contact': 'Tel: (66 38) 685 589',
        'latitude': 12.6953578,
        'longitude': 101.1310336
    },
    'GE': {
        'name': 'Glow Energy',
        'location': '3, I - 4 Road, Map Ta Phut Industrial Estate, Map Ta Phut, Muang District, Rayong 21150, Thailand',
        'contact': 'Tel: (66 38) 684 078-80',
        'latitude': 12.6941877,
        'longitude': 101.1445003
    },
    'G3': {
        'name': 'Glow SPP2&3',
        'location': '11, I - 5 Road, Map Ta Phut Industrial Estate, Map Ta Phut, Muang District, Rayong 21150, Thailand',
        'contact': 'Tel: (66 38) 698 400-10',
        'latitude': 12.6774387,
        'longitude': 101.1364581
    },
    'GH1': {
        'name': 'GHECO-One',
        'location': '11, I - 5 Road, Map Ta Phut Industrial Estate, Map Ta Phut, Muang District, Rayong 21150, Thailand',
        'contact': 'Tel: (66 38) 698 400-10',
        'latitude': 12.675205,
        'longitude': 101.135644
    }
}

@app.route('/')
@app.route('/home')

def home():
    return render_template('home.html', plants=PLANTS)

@app.route('/plant/<key>')
def plant(key):
    plant = PLANTS.get(key)
    from src.models.gaussian_plume import Gaussian
    from src.models.weather import Weather
    wea = Weather("Rayong",plant['latitude'],plant['longitude'])
    obj = Gaussian()
    data = obj.MainCalc(plant['latitude'],plant['longitude'])
    if not plant:
        abort(404)
    return render_template('plant.html', plant=plant,data=data,wind_deg=wea.wind_deg,wind_speed=wea.wind_speed)
# @app.route('/test')
# def test():
#     from src.models.gaussian_plume import Gaussian
#
#     obj = Gaussian()
#     msg = obj.MainCalc(180,5,12.675205,101.135644)
#     return render_template('test.html',msg=msg)

if __name__=='__main__':
    app.run(port=4995, debug=True)
