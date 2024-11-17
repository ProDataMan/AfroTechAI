import requests
import json
import config

# URLs for the APIs
SPORTS_API_BASE_URL = 'https://www.thesportsdb.com/api/v1/json/{}/'.format(config.SPORTS_API_KEY)

# Function to fetch team stats from TheSportsDB
def fetch_team_stats(league_id, seasons):
    team_stats = {}
    for season in seasons:
        print(f"Fetching team data for league {league_id}, season {season}...")
        url = f"{SPORTS_API_BASE_URL}eventsseason.php?id={league_id}&s={season}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if 'events' in data and data['events'] is not None:
                    for event in data['events']:
                        if event['strSport'] == 'American Football':
                            home_team = event['strHomeTeam'].replace(" ", "_")
                            away_team = event['strAwayTeam'].replace(" ", "_")
                            if home_team not in team_stats:
                                team_stats[home_team] = {'wins': 0, 'losses': 0}
                            if away_team not in team_stats:
                                team_stats[away_team] = {'wins': 0, 'losses': 0}
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for team data: {e}")
                print("Raw response text:", response.text)
        else:
            print(f"Error fetching team data: {response.status_code}")
            print("Raw response text:", response.text)
    return team_stats

def calculate_weather_performance(team, weather_condition):
    """
    Calculate historical performance for a team under similar weather conditions.
    """
    # Example mapping of weather conditions to historical performance
    # This should query actual historical game data for more accuracy
    weather_performance = {
        "clear": 0.8,  # Example: 80% win rate in clear weather
        "rain": 0.6,   # Example: 60% win rate in rainy weather
        "snow": 0.5,   # Example: 50% win rate in snowy weather
    }
    return weather_performance.get(weather_condition.lower(), 0.5)  # Default to 50% if no data


def fetch_coordinates(team_name):
    """
    Fetch latitude and longitude for a given NFL team based on its home stadium.
    """
    normalized_team_name = team_name.replace(" ", "_").strip()
    if normalized_team_name in config.TEAM_LOCATIONS:
        return config.TEAM_LOCATIONS[normalized_team_name]["lat"], config.TEAM_LOCATIONS[normalized_team_name]["lon"]
    else:
        print(f"Team location not found for: {normalized_team_name}")
        return None, None
