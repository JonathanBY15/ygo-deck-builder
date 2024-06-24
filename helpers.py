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
    
# Function to calculate card limit
def calculate_card_limit(card):
    """Calculate the card limit."""

    # API ban_tcg, limit mapping
    limit_mapping = {
        'Banned': '0',
        'Limited': '1',
        'Semi-Limited': '2',
        'Unlimited': '3'
    }

    # Get banlist info from card
    if card.get('banlist_info'):
        limit = card['banlist_info']['ban_tcg']
    else:
        limit = 'Unlimited'

    return limit_mapping.get(limit)