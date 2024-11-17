from datetime import datetime
import pytz

# config.py
# API keys
ODDS_API_KEY = '329088a703ba82a2103e7e7c6508500f'
SPORTS_API_KEY = '3'
SPORTSDATAIO_API_KEY = '8e79b8f6532d4d339a4c1c6de17c10dd'
WEATHER_API_KEY = 'f2ec566f92a63397309882acd55bf74a'
NEWS_API_KEY = '168084c7268f48b48f2e4eec0ddca9cd'


ODDS_API_BASE_URL = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/'
SPORTSDATAIO_BASE_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

TEAM_LOCATIONS = {
    "Arizona_Cardinals": {"lat": 33.5276, "lon": -112.2626, "stadium": "State Farm Stadium", "city": "Glendale", "color": "#97233F"},
    "Atlanta_Falcons": {"lat": 33.7554, "lon": -84.4008, "stadium": "Mercedes-Benz Stadium", "city": "Atlanta", "color": "#A71930"},
    "Baltimore_Ravens": {"lat": 39.2779, "lon": -76.6227, "stadium": "M&T Bank Stadium", "city": "Baltimore", "color": "#241773"},
    "Buffalo_Bills": {"lat": 42.7738, "lon": -78.7868, "stadium": "Highmark Stadium", "city": "Orchard Park", "color": "#00338D"},
    "Carolina_Panthers": {"lat": 35.2251, "lon": -80.8531, "stadium": "Bank of America Stadium", "city": "Charlotte", "color": "#0085CA"},
    "Chicago_Bears": {"lat": 41.8623, "lon": -87.6167, "stadium": "Soldier Field", "city": "Chicago", "color": "#0B162A"},
    "Cincinnati_Bengals": {"lat": 39.0954, "lon": -84.5162, "stadium": "Paycor Stadium", "city": "Cincinnati", "color": "#FB4F14"},
    "Cleveland_Browns": {"lat": 41.5061, "lon": -81.6995, "stadium": "Cleveland Browns Stadium", "city": "Cleveland", "color": "#311D00"},
    "Dallas_Cowboys": {"lat": 32.7473, "lon": -97.0945, "stadium": "AT&T Stadium", "city": "Arlington", "color": "#041E42"},
    "Denver_Broncos": {"lat": 39.7439, "lon": -105.0201, "stadium": "Empower Field at Mile High", "city": "Denver", "color": "#FB4F14"},
    "Detroit_Lions": {"lat": 42.3390, "lon": -83.0456, "stadium": "Ford Field", "city": "Detroit", "color": "#0076B6"},
    "Green_Bay_Packers": {"lat": 44.5013, "lon": -88.0622, "stadium": "Lambeau Field", "city": "Green Bay", "color": "#203731"},
    "Houston_Texans": {"lat": 29.6847, "lon": -95.4107, "stadium": "NRG Stadium", "city": "Houston", "color": "#03202F"},
    "Indianapolis_Colts": {"lat": 39.7601, "lon": -86.1639, "stadium": "Lucas Oil Stadium", "city": "Indianapolis", "color": "#002C5F"},
    "Jacksonville_Jaguars": {"lat": 30.3240, "lon": -81.6372, "stadium": "TIAA Bank Field", "city": "Jacksonville", "color": "#101820"},
    "Kansas_City_Chiefs": {"lat": 39.0489, "lon": -94.4839, "stadium": "GEHA Field at Arrowhead Stadium", "city": "Kansas City", "color": "#E31837"},
    "Las_Vegas_Raiders": {"lat": 36.0908, "lon": -115.183, "stadium": "Allegiant Stadium", "city": "Las Vegas", "color": "#A5ACAF"},
    "Los_Angeles_Chargers": {"lat": 33.9534, "lon": -118.3391, "stadium": "SoFi Stadium", "city": "Inglewood", "color": "#002A5E"},
    "Los_Angeles_Rams": {"lat": 33.9534, "lon": -118.3391, "stadium": "SoFi Stadium", "city": "Inglewood", "color": "#003594"},
    "Miami_Dolphins": {"lat": 25.9580, "lon": -80.2389, "stadium": "Hard Rock Stadium", "city": "Miami Gardens", "color": "#008E97"},
    "Minnesota_Vikings": {"lat": 44.9737, "lon": -93.257, "stadium": "U.S. Bank Stadium", "city": "Minneapolis", "color": "#4F2683"},
    "New_England_Patriots": {"lat": 42.0909, "lon": -71.2643, "stadium": "Gillette Stadium", "city": "Foxborough", "color": "#002244"},
    "New_Orleans_Saints": {"lat": 29.9511, "lon": -90.0812, "stadium": "Caesars Superdome", "city": "New Orleans", "color": "#D3BC8D"},
    "New_York_Giants": {"lat": 40.8135, "lon": -74.0745, "stadium": "MetLife Stadium", "city": "East Rutherford", "color": "#0B2265"},
    "New_York_Jets": {"lat": 40.8135, "lon": -74.0745, "stadium": "MetLife Stadium", "city": "East Rutherford", "color": "#125740"},
    "Philadelphia_Eagles": {"lat": 39.9008, "lon": -75.1675, "stadium": "Lincoln Financial Field", "city": "Philadelphia", "color": "#004C54"},
    "Pittsburgh_Steelers": {"lat": 40.4468, "lon": -80.0158, "stadium": "Acrisure Stadium", "city": "Pittsburgh", "color": "#FFB612"},
    "San_Francisco_49ers": {"lat": 37.4030, "lon": -121.9700, "stadium": "Levi's Stadium", "city": "Santa Clara", "color": "#AA0000"},
    "Seattle_Seahawks": {"lat": 47.5952, "lon": -122.3316, "stadium": "Lumen Field", "city": "Seattle", "color": "#002244"},
    "Tampa_Bay_Buccaneers": {"lat": 27.9759, "lon": -82.5033, "stadium": "Raymond James Stadium", "city": "Tampa", "color": "#D50A0A"},
    "Tennessee_Titans": {"lat": 36.1665, "lon": -86.7713, "stadium": "Nissan Stadium", "city": "Nashville", "color": "#0C2340"},
    "Washington_Commanders": {"lat": 38.9078, "lon": -76.8645, "stadium": "FedExField", "city": "Landover", "color": "#773141"}
}

# Function to convert UTC time to Pacific Time
def convert_to_pacific_time(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    pacific_time = utc_time.astimezone(pytz.timezone('US/Pacific'))
    return pacific_time.strftime('%Y-%m-%d %I:%M %p %Z')
# Function to recommend bets based on odds and probabilities

def generate_html(betting_recommendations, css_file="styles.css"):
    """
    Generate HTML content for betting recommendations with dynamic team colors and responsive blocks.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Betting Recommendations</title>
        <link rel="stylesheet" href="{css_file}">
    </head>
    <body>
        <h1>Betting Recommendations</h1>
        <div class="recommendations-container">
    """

    if betting_recommendations:
        for bet in betting_recommendations:
            # Get team colors

            normalized_team_name = bet['recommended_team'].replace(" ", "_").strip()
            if normalized_team_name in TEAM_LOCATIONS:
                recommended_team_color = TEAM_LOCATIONS[normalized_team_name]["color"]
            else:
                print(f"Team location not found for: {normalized_team_name}")

                    
            normalized_team_name = bet['opponent_team'].replace(" ", "_").strip()
            if normalized_team_name in TEAM_LOCATIONS:
                opponent_team_color = TEAM_LOCATIONS[normalized_team_name]["color"]
            else:
                print(f"Team location not found for: {normalized_team_name}")

            html_content += f"""
            <div class="recommendation">
                <div class="team-section" style="color: #ffffff; background-color: {recommended_team_color};">
                    <h2>Bet on: {bet['recommended_team']} ({'Home' if bet['recommended_team'] == bet['home_team'] else 'Away'})</h2>
                </div>
                <div class="team-section" style="color: #ffffff; background-color: {opponent_team_color};">
                    <p><strong>Against:</strong> {bet['opponent_team']} ({'Home' if bet['opponent_team'] == bet['home_team'] else 'Away'})</p>
                </div>
                <p><strong>Game Date:</strong> {bet['game_date']}</p>
                <p><strong>Location:</strong> {bet['location']}</p>
                <p><strong>Expected Value (EV):</strong> {bet['expected_value']:.2f}</p>
                <div class="reasoning">
                    <h3>Reasoning:</h3>
                    <ul>
            """
            for reason in bet['reasoning']:
                html_content += f"<li>{reason}</li>"

            # Add team news if available
            if 'team_news' in bet and bet['team_news']:
                html_content += """
                    </ul>
                </div>
                <div class="news-article">
                    <h3>Team News:</h3>
                    <ul>
                """
                for article in bet['team_news']:
                    html_content += f"""
                        <li>
                            <strong>{article.get('title', 'No Title')}</strong><br>
                            <em>Source: {article.get('source', {}).get('name', 'Unknown')}</em><br>
                            <a href="{article.get('url', '#')}" target="_blank">Read more</a>
                        </li>
                    """
                html_content += """
                    </ul>
                </div>
                """
            else:
                html_content += "</ul></div>"  # Close reasoning div if no news

            html_content += "</div>"  # Close recommendation div

    else:
        html_content += "<p>No positive EV bets found.</p>"

    html_content += """
        </div>
    </body>
    </html>
    """

    # Save to an HTML file
    with open("betting_recommendations.html", "w") as file:
        file.write(html_content)

    print("Betting recommendations have been saved to 'betting_recommendations.html'.")
