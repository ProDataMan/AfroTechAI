import config
import requests
import TeamData
import datetime

def calculate_team_performance_in_weather(team_name, enriched_games):
    """
    Calculate a team's performance in different weather conditions.
    """
    performance = {}
    for game in enriched_games:
        if team_name not in [game['home_team'], game['away_team']]:
            continue
        is_home = team_name == game['home_team']
        condition = game['weather']['condition']
        won = (is_home and game['home_score'] > game['away_score']) or (not is_home and game['away_score'] > game['home_score'])
        if condition not in performance:
            performance[condition] = {'wins': 0, 'losses': 0}
        if won:
            performance[condition]['wins'] += 1
        else:
            performance[condition]['losses'] += 1
    return performance


def fetch_historical_games(team_name, league_id, seasons):
    """
    Fetch historical games for a team from a sports API.
    """
    historical_games = []
    for season in seasons:
        url = f"{config.SPORTS_API_BASE_URL}eventsseason.php?id={league_id}&s={season}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for event in data.get('events', []):
                if event['strHomeTeam'] == team_name or event['strAwayTeam'] == team_name:
                    historical_games.append({
                        "home_team": event['strHomeTeam'],
                        "away_team": event['strAwayTeam'],
                        "date": event['dateEvent'],
                        "stadium": TeamData.TEAM_LOCATIONS.get(event['strHomeTeam'], {}).get("stadium", "Unknown"),
                        "city": TeamData.TEAM_LOCATIONS.get(event['strHomeTeam'], {}).get("city", "Unknown"),
                    })
        else:
            print(f"Error fetching historical games: {response.status_code}")
    return historical_games

def fetch_historical_weather(lat, lon, date):
    """
    Fetch historical weather for a given location and date.
    """
    unix_timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine"
    params = {
        'lat': lat,
        'lon': lon,
        'dt': unix_timestamp,
        'appid': config.WEATHER_API_KEY,
        'units': 'imperial'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "condition": data['current']['weather'][0]['description'],
            "temperature": data['current']['temp']
        }
    else:
        print(f"Error fetching weather for {date}: {response.status_code}")
        return {"condition": "unknown", "temperature": "N/A"}


def merge_games_with_weather(historical_games):
    """
    Add weather data to historical game records.
    """
    enriched_games = []
    for game in historical_games:
        home_team = game['home_team'].replace(" ", "_")
        location = TeamData.TEAM_LOCATIONS.get(home_team, {})
        lat, lon = location.get('lat'), location.get('lon')
        if not lat or not lon:
            continue
        weather = fetch_historical_weather(lat, lon, game['date'])
        game['weather'] = weather
        enriched_games.append(game)
    return enriched_games
