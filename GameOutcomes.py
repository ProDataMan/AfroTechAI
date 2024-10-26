import requests
import json
from datetime import datetime
import pytz

# API keys
ODDS_API_KEY = '329088a703ba82a2103e7e7c6508500f'
SPORTS_API_KEY = '3'
SPORTSDATAIO_API_KEY = 'e19e0cfff5a84ca2900f667e5db7f5ad'

# URLs for the APIs
SPORTS_API_BASE_URL = 'https://www.thesportsdb.com/api/v1/json/{}/'.format(SPORTS_API_KEY)
ODDS_API_BASE_URL = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/'
SPORTSDATAIO_BASE_URL = 'https://api.sportsdata.io/v3/nfl/scores/json/'

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

# Function to fetch recent events data from TheSportsDB
def fetch_recent_events(league_id, season):
    print(f"Fetching recent events for league {league_id}, season {season}...")
    url = f"{SPORTS_API_BASE_URL}eventsseason.php?id={league_id}&s={season}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'events' in data and data['events'] is not None:
                return [event for event in data['events'] if event['strSport'] == 'American Football']
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for recent events: {e}")
            print("Raw response text:", response.text)
    else:
        print(f"Error fetching recent events: {response.status_code}")
        print("Raw response text:", response.text)
    return []

# Function to fetch next 5 scheduled events for the league
def fetch_upcoming_events(league_id):
    print(f"Fetching next 5 scheduled events for league {league_id}...")
    url = f"{SPORTS_API_BASE_URL}eventsnextleague.php?id={league_id}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'events' in data and data['events'] is not None:
                return [event for event in data['events'] if event['strSport'] == 'American Football'][:5]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for upcoming events: {e}")
            print("Raw response text:", response.text)
    else:
        print(f"Error fetching upcoming events: {response.status_code}")
        print("Raw response text:", response.text)
    return []

# Function to fetch odds data from Odds API
def fetch_odds():
    print("Fetching odds data...")
    url = f"{ODDS_API_BASE_URL}?apiKey={ODDS_API_KEY}&regions=us&markets=h2h"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for odds data: {e}")
            print("Raw response text:", response.text)
    else:
        print(f"Error fetching odds: {response.status_code}")
        print("Raw response text:", response.text)
    return []

# Function to fetch player stats and injury reports from SportsDataIO
def fetch_player_stats_and_injuries():
    print("Fetching player stats and injury reports...")
    url = f"{SPORTSDATAIO_BASE_URL}PlayerSeasonStats/2023REG?key={SPORTSDATAIO_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for player stats and injuries: {e}")
            print("Raw response text:", response.text)
    else:
        print(f"Error fetching player stats and injuries: {response.status_code}")
        print("Raw response text:", response.text)
    return []

# Function to update team stats based on recent events
def update_team_stats(team_stats, events):
    print("Updating team stats based on recent events...")
    for event in events:
        if event['intHomeScore'] is not None and event['intAwayScore'] is not None:
            home_team = event['strHomeTeam'].replace(" ", "_")
            away_team = event['strAwayTeam'].replace(" ", "_")
            home_score = int(event['intHomeScore'])
            away_score = int(event['intAwayScore'])

            if home_team in team_stats and away_team in team_stats:
                if home_score > away_score:
                    team_stats[home_team]['wins'] += 1
                    team_stats[away_team]['losses'] += 1
                elif away_score > home_score:
                    team_stats[away_team]['wins'] += 1
                    team_stats[home_team]['losses'] += 1

# Function to calculate win probabilities
def calculate_win_probability(team, team_stats):
    if team in team_stats:
        total_games = team_stats[team]['wins'] + team_stats[team]['losses']
        if total_games > 0:
            return team_stats[team]['wins'] / total_games
    return 0.0

# Function to convert UTC time to Pacific Time
def convert_to_pacific_time(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    pacific_time = utc_time.astimezone(pytz.timezone('US/Pacific'))
    return pacific_time.strftime('%Y-%m-%d %I:%M %p %Z')

# Function to recommend bets based on odds and probabilities
def recommend_bets(team_stats, odds_data, weather_data, player_news):
    betting_recommendations = []
    for game in odds_data:
        home_team = game['home_team'].replace(" ", "_")
        away_team = game['away_team'].replace(" ", "_")
        game_date = convert_to_pacific_time(game['commence_time'])
        print(f"Calculating for match: {home_team} vs {away_team} on {game_date}")

        home_win_prob = calculate_win_probability(home_team, team_stats)
        away_win_prob = calculate_win_probability(away_team, team_stats)

        home_odds = None
        away_odds = None

        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    home_odds, away_odds = market['outcomes'][0]['price'], market['outcomes'][1]['price']
                    break

        if home_odds is None or away_odds is None:
            continue

        # Calculate Expected Value (EV)
        home_ev = (home_win_prob * home_odds) - 1
        away_ev = (away_win_prob * away_odds) - 1

        # Build reasoning for the bet
        reasoning = []
        if home_ev > 0:
            reasoning.append(f"Bet on {home_team} because their win probability is higher than the odds suggest.")
            if weather_data.get(game_date, {}).get('condition') == 'rain':
                reasoning.append(f"{home_team} typically struggles in the rain.")
            if player_news.get(home_team):
                reasoning.append(f"Recent news: {player_news[home_team]}")
            if home_team in team_stats and away_team in team_stats:
                if team_stats[home_team]['wins'] < team_stats[away_team]['wins']:
                    reasoning.append(f"Historically, {away_team} has a better record against {home_team}.")

        if away_ev > 0:
            reasoning.append(f"Bet on {away_team} because their win probability is higher than the odds suggest.")
            if weather_data.get(game_date, {}).get('condition') == 'rain':
                reasoning.append(f"{away_team} typically performs well in rainy conditions.")
            if player_news.get(away_team):
                reasoning.append(f"Recent news: {player_news[away_team]}")
            if away_team in team_stats and home_team in team_stats:
                if team_stats[away_team]['wins'] < team_stats[home_team]['wins']:
                    reasoning.append(f"Historically, {home_team} has a better record against {away_team}.")

        if reasoning:
            betting_recommendations.append((home_team if home_ev > 0 else away_team, game_date, home_ev if home_ev > 0 else away_ev, reasoning))

    return betting_recommendations

# Main function to run the analysis
def main():
    league_id = '4391'  # Corrected league ID for TheSportsDB (NFL)
    seasons = ['2020', '2021', '2022', '2023']

    team_stats = fetch_team_stats(league_id, seasons)
    for season in seasons:
        recent_events = fetch_recent_events(league_id, season)
        update_team_stats(team_stats, recent_events)
    print("Final team stats:", team_stats)

    # Fetch player stats and injury data
    player_data = fetch_player_stats_and_injuries()
    print("Player Data:", player_data)

    # Adjust team stats based on player injuries
    for player in player_data:
        team = player['Team']['Name'].replace(" ", "_")
        if team in team_stats:
            if player['InjuryStatus'] == 'Out':
                team_stats[team]['adjusted'] = True  # Example adjustment

    odds_data = fetch_odds()
    
    # Example weather data and player news (you'll need to implement fetching this data)
    weather_data = {
        "2023-10-02T00:00:00Z": {"condition": "rain"},  # Example date
    }
    player_news = {
        "Tampa_Bay": "Quarterback was arrested last week for fighting in a bar.",
        "Baltimore": "No significant news.",
    }

    betting_recommendations = recommend_bets(team_stats, odds_data, weather_data, player_news)

    if betting_recommendations:
        print("Betting Recommendations:")
        for bet in betting_recommendations:
            print(f"Bet on {bet[0]} in game on {bet[1]} with EV: {bet[2]:.2f}. Reasoning: {'; '.join(bet[3])}")
    else:
        print("No positive EV bets found.")

    # Predict upcoming games
    upcoming_events = fetch_upcoming_events(league_id)
    if upcoming_events:
        print("\nPredictions for Upcoming Games:")
        for event in upcoming_events:
            home_team = event['strHomeTeam'].replace(" ", "_")
            away_team = event['strAwayTeam'].replace(" ", "_")
            home_win_prob = calculate_win_probability(home_team, team_stats)
            away_win_prob = calculate_win_probability(away_team, team_stats)
            event_date = convert_to_pacific_time(event['dateEvent'] + 'T00:00:00Z')
            print(f"{home_team} vs {away_team} on {event_date}: {home_team} Win Probability: {home_win_prob:.2%}, {away_team} Win Probability: {away_win_prob:.2%}")

if __name__ == "__main__":
    main()
