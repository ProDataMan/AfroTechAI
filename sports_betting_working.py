import requests
import json

# API keys
ODDS_API_KEY = '329088a703ba82a2103e7e7c6508500f'
SPORTS_API_KEY = '3'

# URLs for the APIs
SPORTS_API_BASE_URL = 'https://www.thesportsdb.com/api/v1/json/{}/'.format(SPORTS_API_KEY)
ODDS_API_BASE_URL = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/'

# Function to fetch team stats from TheSportsDB
def fetch_team_stats(league_id, season):
    team_stats = {}
    print(f"Fetching team data for league {league_id}...")
    url = f"{SPORTS_API_BASE_URL}eventsseason.php?id={league_id}&s={season}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'events' in data and data['events'] is not None:
                for event in data['events']:
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
                return data['events']
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for recent events: {e}")
            print("Raw response text:", response.text)
    else:
        print(f"Error fetching recent events: {response.status_code}")
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

# Function to recommend bets based on odds and probabilities
def recommend_bets(team_stats, odds_data):
    betting_recommendations = []
    for game in odds_data:
        home_team = game['home_team'].replace(" ", "_")
        away_team = game['away_team'].replace(" ", "_")
        print(f"Calculating for match: {home_team} vs {away_team}")

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

        print(f"{home_team} Win Probability: {home_win_prob:.2f}")
        print(f"{away_team} Win Probability: {away_win_prob:.2f}")
        print(f"{home_team} Expected Value (EV): {home_ev:.2f}")
        print(f"{away_team} Expected Value (EV): {away_ev:.2f}")

        if home_ev > 0:
            betting_recommendations.append((home_team, game['id'], home_ev))
        if away_ev > 0:
            betting_recommendations.append((away_team, game['id'], away_ev))

    return betting_recommendations

# Main function to run the analysis
def main():
    league_id = '4391'  # Corrected league ID for TheSportsDB
    season = '2023'

    team_stats = fetch_team_stats(league_id, season)
    recent_events = fetch_recent_events(league_id, season)
    update_team_stats(team_stats, recent_events)
    print("Final team stats:", team_stats)

    odds_data = fetch_odds()
    betting_recommendations = recommend_bets(team_stats, odds_data)

    if betting_recommendations:
        print("Betting Recommendations:")
        for bet in betting_recommendations:
            print(f"Bet on {bet[0]} in game {bet[1]} with EV: {bet[2]:.2f}")
    else:
        print("No positive EV bets found.")

if __name__ == "__main__":
    main()
