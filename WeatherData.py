import requests
import TeamData
import pytz
from datetime import datetime
import config

def fetch_weather_data(home_team, game_date):
    """
    Fetch weather data for a location inferred from the home team and game date.
    Dynamically uses historical weather API for past dates and forecast API for future dates.
    """
    print(f"Home Team: {home_team} game date: {game_date}")

    naive_game_datetime = datetime.strptime(game_date[:-4], '%Y-%m-%d %I:%M %p')
    timezone = pytz.timezone('US/Pacific')  # Assuming 'PST' is Pacific Time
    game_datetime = timezone.localize(naive_game_datetime)
    game_timestamp = int(game_datetime.timestamp())
    current_timestamp = int(datetime.now().timestamp())

    # Fetch coordinates dynamically based on the home team
    lat, lon = TeamData.fetch_coordinates(home_team)
    if not lat or not lon:
        print(f"Error: Invalid coordinates for team {home_team}")
        return {"condition": "unknown", "temperature": 70}

    # Determine API endpoint based on game date
    if game_timestamp <= current_timestamp:
        params = {
            'lat': lat,
            'lon': lon,
            'dt': game_timestamp,
            'appid': config.WEATHER_API_KEY,
            'units': 'imperial'
        }
        url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
    else:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': config.WEATHER_API_KEY,
            'units': 'imperial'
        }
        url = "https://api.openweathermap.org/data/2.5/forecast"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        if game_timestamp <= current_timestamp:
            return {
                'condition': weather_data['current']['weather'][0]['main'],
                'temperature': weather_data['current']['temp']
            }
        else:
            closest_forecast = min(
                weather_data.get("list", []),
                key=lambda f: abs(game_datetime.timestamp() - datetime.strptime(f["dt_txt"], '%Y-%m-%d %H:%M:%S').timestamp()),
                default=None
            )
            if closest_forecast:
                return {
                    'condition': closest_forecast['weather'][0]['main'],
                    'temperature': closest_forecast['main']['temp']
                }
    else:
        print(f"Error fetching weather data: {response.status_code}, Response: {response.text}")
        return {"condition": "unknown", "temperature": 70}


