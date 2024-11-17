import requests
import config
import json

# Function to fetch player stats and injury reports from SportsDataIO
def fetch_player_stats_and_injuries():
    print("Fetching player stats and injury reports...")
    url = f"{config.SPORTSDATAIO_BASE_URL}PlayerSeasonStats/2024REG?key={config.SPORTSDATAIO_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            # print("Fetched Player Data:", json.dumps(data, indent=2))  # Debugging step
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for player stats and injuries: {e}")
            print("Raw response text:", response.text)
    else:
        print(f"Error fetching player stats and injuries: {response.status_code}")
        # print("Raw response text:", response.text)
    return 

def fetch_player_news(player_name):
    NEWS_API_URL = f'https://newsapi.org/v2/everything?q={player_name}&apiKey={config.NEWS_API_KEY}'
    print(f"News URL: {NEWS_API_URL}")

    response = requests.get(NEWS_API_URL)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching player news data for {player_name}: {response.status_code}")
        return []
