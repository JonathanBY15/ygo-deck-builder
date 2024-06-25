import requests
from models import db, Card

# Function to fetch cards from API
def fetch_ygo_cards(fname="", type=None, attribute=None, race=None, level=None, attack=None, defense=None, num=20, offset=0):
    """Fetch Yu-Gi-Oh! cards from API by 'fname'."""
    # url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?&num=20&offset=0"
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

    params = {
        "fname": fname,
        "num": num,
        "offset": offset
    }

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
        # return data['data']
        return data
    else:
        print("No cards match the filters.")
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


# Function to add card to database
def add_card_to_db(card):
    """Add a card to the database if it does not already exist in the database. Return the card."""

    # Check if card already exists
    existing_card = Card.query.filter_by(name=card['name']).first()

    if existing_card:
        return existing_card

    # Create a new card
    new_card = Card(
        name=card['name'],
        type=card['type'],
        attribute=card['attribute'],
        race=card['race'],
        level=card['level'],
        attack=card['atk'],
        defense=card['def'],
        description=card['desc'],
        img_url=card['card_images'][0]['image_url'],
        limit=calculate_card_limit(card)
    )

    db.session.add(new_card)
    db.session.commit()

    return new_card
