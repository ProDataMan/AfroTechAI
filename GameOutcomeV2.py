import requests
import json
from datetime import datetime
import config
import pytz  # For timezone handling

# URLs for the APIs
SPORTS_API_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{config.SPORTS_API_KEY}/"
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/"
SPORTSDATAIO_BASE_URL = "https://api.sportsdata.io/v3/nfl/stats/json/"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

TEAM_LOCATIONS = {
    "Arizona_Cardinals": {"lat": 33.5276, "lon": -112.2626},
    "Atlanta_Falcons": {"lat": 33.7554, "lon": -84.4008},
    "Baltimore_Ravens": {"lat": 39.2779, "lon": -76.6227},
    "Buffalo_Bills": {"lat": 42.7738, "lon": -78.7868},
    "Carolina_Panthers": {"lat": 35.2251, "lon": -80.8531},
    "Chicago_Bears": {"lat": 41.8623, "lon": -87.6167},
    "Cincinnati_Bengals": {"lat": 39.0954, "lon": -84.5162},
    "Cleveland_Browns": {"lat": 41.5061, "lon": -81.6995},
    "Dallas_Cowboys": {"lat": 32.7473, "lon": -97.0945},
    "Denver_Broncos": {"lat": 39.7439, "lon": -105.0201},
    "Detroit_Lions": {"lat": 42.339, "lon": -83.0456},
    "Green_Bay_Packers": {"lat": 44.5013, "lon": -88.0622},
    "Houston_Texans": {"lat": 29.6847, "lon": -95.4107},
    "Indianapolis_Colts": {"lat": 39.7601, "lon": -86.1639},
    "Jacksonville_Jaguars": {"lat": 30.324, "lon": -81.6372},
    "Kansas_City_Chiefs": {"lat": 39.0489, "lon": -94.4839},
    "Las_Vegas_Raiders": {"lat": 36.0908, "lon": -115.183},
    "Los_Angeles_Chargers": {"lat": 33.9534, "lon": -118.3391},
    "Los_Angeles_Rams": {"lat": 33.9534, "lon": -118.3391},
    "Miami_Dolphins": {"lat": 25.958, "lon": -80.2389},
    "Minnesota_Vikings": {"lat": 44.9737, "lon": -93.257},
    "New_England_Patriots": {"lat": 42.0909, "lon": -71.2643},
    "New_Orleans_Saints": {"lat": 29.9511, "lon": -90.0812},
    "New_York_Giants": {"lat": 40.8135, "lon": -74.0745},
    "New_York_Jets": {"lat": 40.8135, "lon": -74.0745},
    "Philadelphia_Eagles": {"lat": 39.9008, "lon": -75.1675},
    "Pittsburgh_Steelers": {"lat": 40.4468, "lon": -80.0158},
    "San_Francisco_49ers": {"lat": 37.403, "lon": -121.97},
    "Seattle_Seahawks": {"lat": 47.5952, "lon": -122.3316},
    "Tampa_Bay_Buccaneers": {"lat": 27.9759, "lon": -82.5033},
    "Tennessee_Titans": {"lat": 36.1665, "lon": -86.7713},
    "Washington_Commanders": {"lat": 38.9078, "lon": -76.8645},
}

# Normalize team names
def normalize_team_name(team_name):
    return team_name.replace(" ", "_").strip()

# Fetch team coordinates
def fetch_coordinates(team_name):
    normalized_team_name = normalize_team_name(team_name)
    if normalized_team_name in TEAM_LOCATIONS:
        return TEAM_LOCATIONS[normalized_team_name]["lat"], TEAM_LOCATIONS[normalized_team_name]["lon"]
    else:
        print(f"Team location not found for: {normalized_team_name}")
        return None, None

# Convert UTC to Pacific Time
def convert_to_pacific_time(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    pacific_time = utc_time.astimezone(pytz.timezone('US/Pacific'))
    return pacific_time.strftime('%Y-%m-%d %I:%M %p %Z')

# Fetch weather data
def fetch_weather_data(home_team, game_date):
    naive_game_datetime = datetime.strptime(game_date[:-4], '%Y-%m-%d %I:%M %p')
    timezone = pytz.timezone('US/Pacific')
    game_datetime = timezone.localize(naive_game_datetime)
    game_timestamp = int(game_datetime.timestamp())
    current_timestamp = int(datetime.now().timestamp())

    lat, lon = fetch_coordinates(home_team)
    if not lat or not lon:
        return {"condition": "unknown", "temperature": "N/A"}

    if game_timestamp <= current_timestamp:
        params = {
            "lat": lat,
            "lon": lon,
            "dt": game_timestamp,
            "appid": config.WEATHER_API_KEY,
            "units": "imperial"
        }
        url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
    else:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": config.WEATHER_API_KEY,
            "units": "imperial"
        }
        url = "https://api.openweathermap.org/data/2.5/forecast"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        if game_timestamp <= current_timestamp:
            return {
                "condition": weather_data["current"]["weather"][0]["description"],
                "temperature": weather_data["current"]["temp"]
            }
        else:
            closest_forecast = min(
                weather_data.get("list", []),
                key=lambda f: abs(game_datetime.timestamp() - datetime.strptime(f["dt_txt"], '%Y-%m-%d %H:%M:%S').timestamp()),
                default=None
            )
            if closest_forecast:
                return {
                    "condition": closest_forecast["weather"][0]["description"],
                    "temperature": closest_forecast["main"]["temp"]
                }
    print(f"Error fetching weather data: {response.status_code}")
    return {"condition": "unknown", "temperature": "N/A"}

# Recommend bets based on data
def recommend_bets(team_stats, odds_data, player_data):
    betting_recommendations = []
    for game in odds_data:
        home_team = normalize_team_name(game["home_team"])
        away_team = normalize_team_name(game["away_team"])
        game_date = convert_to_pacific_time(game["commence_time"])

        weather = fetch_weather_data(home_team, game_date) or {"condition": "clear", "temperature": 70}
        print(f"Calculating for match: {home_team} vs {away_team} on {game_date}")

        home_win_prob = team_stats.get(home_team, {}).get("wins", 0) / max(
            1, team_stats.get(home_team, {}).get("wins", 0) + team_stats.get(home_team, {}).get("losses", 0)
        )
        away_win_prob = team_stats.get(away_team, {}).get("wins", 0) / max(
            1, team_stats.get(away_team, {}).get("wins", 0) + team_stats.get(away_team, {}).get("losses", 0)
        )

        home_ev = home_win_prob * game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"] - 1
        away_ev = away_win_prob * game["bookmakers"][0]["markets"][0]["outcomes"][1]["price"] - 1

        if home_ev > 0:
            betting_recommendations.append(
                f"Bet on {home_team}. Weather: {weather['condition']}, {weather['temperature']}°F"
            )
        if away_ev > 0:
            betting_recommendations.append(
                f"Bet on {away_team}. Weather: {weather['condition']}, {weather['temperature']}°F"
            )

    return betting_recommendations

# Main function
def main():
    league_id = "4391"
    seasons = ["2020", "2021", "2022", "2023"]

    # Fetch team stats (example function call)
    team_stats = fetch_team_stats(league_id, seasons)

    # Fetch odds data
    odds_data = fetch_odds()

    # Fetch player stats and injuries
    player_data = fetch_player_stats_and_injuries()

    # Get betting recommendations
    betting_recommendations = recommend_bets(team_stats, odds_data, player_data)
    print("Betting Recommendations:")
    for bet in betting_recommendations:
        print(bet)

if __name__ == "__main__":
    main()
