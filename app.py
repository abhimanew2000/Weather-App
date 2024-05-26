from flask import Flask, jsonify, request, render_template
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'


@app.route('/')
def index():
    return render_template('weather.html')


@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # You can change to 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    forecast_response = requests.get(FORECAST_URL, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to get weather data'}), response.status_code
    
    if forecast_response.status_code != 200:
        return jsonify({'error': 'Failed to get forecast data'}), response.status_code

    data = response.json()
    forecast_data = forecast_response.json()

    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'coord': data['coord'],  # Include coordinates in the weather data
        'hourly': forecast_data['list'][:2]  # Get the first 12 hourly forecasts
    }
    
    return render_template('weather.html', weather=weather)


if __name__ == '__main__':
    app.run(debug=True)
