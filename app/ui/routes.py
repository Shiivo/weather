from flask import Blueprint, render_template, request, redirect
import pytz
import requests
import configparser
from app.models import db, Result
from datetime import datetime as dt

ui_bp = Blueprint(
  'ui_bp', __name__,
  template_folder='templates',
  static_folder='static'
)


@ui_bp.route('/')
def home():
    return render_template("home.html")


@ui_bp.route('/result', methods=['POST'])
def render_results():
    api_key = 'b473bf7eb5df087470cc26c84fe5ac05'
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
    #us_c = dt.now(pytz.timezone('America/Mexico_City'))
    us_p = dt.now(pytz.timezone('America/Tijuana'))
    #us_e = dt.now(pytz.timezone('America/New_York'))
    #us_m = dt.now(pytz.timezone('America/Chihuahua'))
    dt_obj = dt.now()

    result = Result(us_p=us_p, feels_like=feels_like, dt_obj=dt_obj,  temp=temp, weather=weather, location=location)
    db.session.add(result)
    db.session.commit()
    return render_template('result.html',
                           location=location, temp=temp, us_p=us_p,
                           feels_like=feels_like, weather=weather, icon_url=icon_url)



def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

@ui_bp.route('/results', methods=['POST'])
def list_results():
   results = Result.query
   return render_template('results.html', results=results)


@ui_bp.route('/api/results')
def results_all():
    return {'data': [result.to_dict() for result in Result.query]}
