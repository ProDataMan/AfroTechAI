import requests
import json
import config
import TeamData

def recommend_bets(team_stats, odds_data, weather_data, player_data, player_news):
    """
    Recommend bets based on odds, team performance, weather, player injuries, and past performance.
    """
    betting_recommendations = []
    
    for game in odds_data:
        home_team = game['home_team'].replace(" ", "_")
        away_team = game['away_team'].replace(" ", "_")
        game_date = config.convert_to_pacific_time(game['commence_time'])
        location = config.TEAM_LOCATIONS.get(home_team, {"stadium": "Unknown Stadium", "city": "Unknown City"})

        print(f"Calculating for match: {home_team} vs {away_team} on {game_date} at {location['stadium']}, {location['city']}")

        # Fetch weather data for the game
        game_weather = weather_data.get(home_team + "_" + game_date, {"condition": "unknown", "temperature": "N/A"})

        # Calculate win probabilities
        home_win_prob = calculate_win_probability(home_team, team_stats)
        away_win_prob = calculate_win_probability(away_team, team_stats)

        # Gather injury information
        home_injuries = [
            p for p in player_data
            if isinstance(p, dict) and p.get('Team') == home_team and p.get('InjuryStatus') == 'Out'
        ]
        away_injuries = [
            p for p in player_data
            if isinstance(p, dict) and p.get('Team') == away_team and p.get('InjuryStatus') == 'Out'
        ]

        # Calculate expected value
        home_odds = next((outcome['price'] for outcome in game['bookmakers'][0]['markets'][0]['outcomes'] if outcome['name'] == game['home_team']), None)
        away_odds = next((outcome['price'] for outcome in game['bookmakers'][0]['markets'][0]['outcomes'] if outcome['name'] == game['away_team']), None)

        if home_odds is None or away_odds is None:
            print(f"Odds not found for game: {home_team} vs {away_team}")
            continue

        home_ev = (home_win_prob * home_odds) - 1
        away_ev = (away_win_prob * away_odds) - 1

        # Build reasoning for home and away teams
        def build_reasoning(team, is_home):
            """
            Build reasoning for the given team (home or away).
            """
            team_type = "Home" if is_home else "Away"
            reasoning = [f"Bet on: ({team_type}) {team.replace('_', ' ')}."]
            reasoning.append(f"Weather: {game_weather.get('condition', 'unknown')}, {game_weather.get('temperature', 'N/A')}&deg;F.")
            # Add injuries if any
            injuries = home_injuries if is_home else away_injuries
            if injuries:
                injury_details = "; ".join([f"{p['Name']} ({p['Position']}): {p['InjuryStatus']} - {p.get('Injury', 'No details')}" for p in injuries])
                reasoning.append(f"Injuries: {injury_details}.")
            
            # Add team news
            team_news = player_news.get(team, "No significant news.")
            reasoning.append(f"Team News: {team_news}")
            
            # Add past performance in similar weather if available
            past_performance = team_stats.get(team, {}).get('performance_in_similar_weather', "No data available.")
            reasoning.append(f"Past Performance in Similar Weather: {past_performance}.")
            
            return reasoning

        # Add recommendations based on EV
        if home_ev > 0:
            betting_recommendations.append({
                "recommended_team": home_team,
                "opponent_team": away_team,
                "home_team": home_team,
                "away_team": away_team,
                "game_date": game_date,
                "location": f"{location['stadium']}, {location['city']}",
                "expected_value": home_ev,
                "reasoning": build_reasoning(home_team, is_home=True)
            })
        if away_ev > 0:
            betting_recommendations.append({
                "recommended_team": away_team,
                "opponent_team": home_team,
                "home_team": home_team,
                "away_team": away_team,
                "game_date": game_date,
                "location": f"{location['stadium']}, {location['city']}",
                "expected_value": away_ev,
                "reasoning": build_reasoning(away_team, is_home=False)
            })

    return betting_recommendations

# Function to fetch odds data from Odds API
def fetch_odds():
    print("Fetching odds data...")
    url = f"{config.ODDS_API_BASE_URL}?apiKey={config.ODDS_API_KEY}&regions=us&markets=h2h"
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

[]


# Function to calculate win probabilities
def calculate_win_probability(team, team_stats):
    if team in team_stats:
        total_games = team_stats[team]['wins'] + team_stats[team]['losses']
        if total_games > 0:
            return team_stats[team]['wins'] / total_games
    return 0.0