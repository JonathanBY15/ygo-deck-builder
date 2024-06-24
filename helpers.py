import requests

# Function to fetch cards from API
def fetch_ygo_cards(fname="", type=None, attribute=None, race=None, level=None, attack=None, defense=None):
    """Fetch Yu-Gi-Oh! cards from API by 'fname'."""
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

    params = {"fname": fname}

    if type:
        params["type"] = type
    if attribute:
        params["attribute"] = attribute
    if race:
        params["race"] = race
    if level:
        params["level"] = level
    if attack:
        params["atk"] = attack
    if defense:
        params["def"] = defense

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error fetching data. Status code: {response.status_code}")
        return None