import requests
import pandas as pd

API_KEY = '3'
LEAGUE_ID = '4391'  # NFL League ID on SportsDB
seasons = [str(year) for year in range(2013, 2023)]  # Last 10 years

rows = []

for season in seasons:
    URL = f'https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsseason.php?id={LEAGUE_ID}&s={season}'
    response = requests.get(URL)
    data = response.json()

    if 'events' in data and data['events']:
        games = data['events']
        for game in games:
            rows.append({
                'Date': game['dateEvent'],
                'Season': season,
                'HomeTeam': game['strHomeTeam'],
                'AwayTeam': game['strAwayTeam'],
                'HomeScore': game['intHomeScore'],
                'AwayScore': game['intAwayScore']
            })

# Convert to DataFrame
df = pd.DataFrame(rows)
df.to_csv('nfl_historical_data_last_10_years.csv', index=False)