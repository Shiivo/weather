from flask import Flask, render_template, request
from datetime import datetime as dt
from app.models import db
import pytz
import requests
import configparser


app = Flask(__name__)
app.debug = True
app.config.from_object('config')
db.init_app(app)
db.create_all()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    api_key = get_api_key()
    zip_code = request.form['zipCode']
    temp_unit = request.form['temp_unit']

    if temp_unit == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
    else:
        data = get_weather_results_metric(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = f"{data['main']['feels_like']:.2f}"
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]
    icon_url = "https://openweathermap.org/img/w/" + icon + ".png"
    us_c = dt.now(pytz.timezone('America/Mexico_City'))
    us_p = dt.now(pytz.timezone('America/Tijuana'))
    us_e = dt.now(pytz.timezone('America/New_York'))
    us_m = dt.now(pytz.timezone('America/Chihuahua'))

    return render_template('result.html',
                           location=location, temp=temp, us_c=us_c, us_p=us_p, us_e=us_e, us_m=us_m,
                           feels_like=feels_like, weather=weather, icon_url=icon_url)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


print(get_weather_results_imperial("95129", get_api_key()))

print(get_weather_results_metric("95129", get_api_key()))
