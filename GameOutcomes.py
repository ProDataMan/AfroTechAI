import requests
import json
import config
import PlayerData
import GameData
import pytz  # For timezone handling
import TeamData
import BetData
import WeatherData

# URLs for the APIs
SPORTS_API_BASE_URL = 'https://www.thesportsdb.com/api/v1/json/{}/'.format(config.SPORTS_API_KEY)

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

# Main function to run the analysis
def main():
    league_id = '4391'  # Corrected league ID for TheSportsDB (NFL)
    seasons = ['2020', '2021', '2022', '2023']

    # Fetch and update team stats
    team_stats = TeamData.fetch_team_stats(league_id, seasons)
    for season in seasons:
        recent_events = fetch_recent_events(league_id, season)
        update_team_stats(team_stats, recent_events)

    # Fetch player stats and injury data
    player_data = PlayerData.fetch_player_stats_and_injuries()

    # Fetch odds data
    odds_data = BetData.fetch_odds()

    # Fetch player news dynamically for teams in the odds data
    teams = set([game['home_team'].replace(" ", "_") for game in odds_data] +
                [game['away_team'].replace(" ", "_") for game in odds_data])
    player_news = {team: PlayerData.fetch_player_news(team) for team in teams}

    # Fetch weather data dynamically for each game
    weather_data = {}
    for game in odds_data:
        home_team = game['home_team'].replace(" ", "_")
        game_date = config.convert_to_pacific_time(game['commence_time'])
        weather_data_key = f"{home_team}_{game_date}"
        weather_data[weather_data_key] = WeatherData.fetch_weather_data(home_team, game_date)
     
    # Generate betting recommendations
    betting_recommendations = BetData.recommend_bets(team_stats, odds_data, weather_data, player_data, player_news)

    # Print betting recommendations
    if betting_recommendations:
        print("Betting Recommendations:")
        for bet in betting_recommendations:
            # Determine if the recommended and opponent teams are Home or Away
            recommended_team_type = "Home" if bet['recommended_team'] == bet['home_team'] else "Away"
            opponent_team_type = "Home" if bet['opponent_team'] == bet['home_team'] else "Away"

            # Print the main recommendation details
            print(f"Bet on: {bet['recommended_team']} ({recommended_team_type})")
            print(f"Against: {bet['away_team' if bet['recommended_team'] == bet['home_team'] else 'home_team']} ({opponent_team_type})")
            print(f"Game Date: {bet['game_date']}")
            print(f"Location: {bet['location']}")
            print(f"Expected Value (EV): {bet['expected_value']:.2f}")

            # Print reasoning with clear bullet points
            print("Reasoning:")
            for reason in bet['reasoning']:
                print(f"- {reason}")
            print("\n")  # Add a line break between each recommendation for better readability
    else:
        print("No positive EV bets found.")


    # Generate HTML for betting recommendations
    config.generate_html(betting_recommendations)

    # Predict upcoming games
    upcoming_events = fetch_upcoming_events(league_id)
    if upcoming_events:
        print("\nPredictions for Upcoming Games:")
        for event in upcoming_events:
            home_team = event['strHomeTeam'].replace(" ", "_")
            away_team = event['strAwayTeam'].replace(" ", "_")
            home_win_prob = config.calculate_win_probability(home_team, team_stats)
            away_win_prob = config.calculate_win_probability(away_team, team_stats)
            event_date = config.convert_to_pacific_time(event['dateEvent'] + 'T00:00:00Z')
            print(f"{home_team} vs {away_team} on {event_date}:")
            print(f"  {home_team} Win Probability: {home_win_prob:.2%}")
            print(f"  {away_team} Win Probability: {away_win_prob:.2%}")


if __name__ == "__main__":
    main()
