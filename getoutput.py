import requests

# Replace this with your actual API key from TheSportsDB
api_key = '3'

def get_team_stats():

    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/lookuptable.php?l=4328&s=2022-2023"  # Replace with the league ID and season
    response = requests.get(url)
    
    # Parse the response
    data = response.json()
    
    # Print the response to see the structure
    print(data)
    
    # Create a dictionary for team stats
    team_stats = {}
    for team in data['table']:
        print(team)  # Print each team's data to check available fields
        team_name = team['name']  # This might need to be updated based on the actual key
        wins = int(team['win'])
        losses = int(team['loss'])
        team_stats[team_name] = {'wins': wins, 'losses': losses}
    
    return team_stats
