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
    
# Function to fetch card by ID
def fetch_card_by_id(id):
    """Fetch a Yu-Gi-Oh! card by 'id'."""
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]
    else:
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
        id=card['id'],
        name=card['name'],
        type=card['type'],
        attribute=card.get('attribute', None),
        race=card.get('race', None),
        level=card.get('level', None),
        attack=card.get('atk', None),
        defense=card.get('def', None),
        description=card.get('desc', ''),
        img_url=card['card_images'][0]['image_url'],
        limit=calculate_card_limit(card),
        extra_deck=is_extra_deck(card)
    )

    db.session.add(new_card)
    db.session.commit()

    return new_card

# Map card type to main deck or extra deck
card_type_to_deck = {
    'Skill Card': False,
    'Spell Card': False,
    'Trap Card': False,
    'Normal Monster': False,
    'Normal Tuner Monster': False,
    'Effect Monster': False,
    'Tuner Monster': False,
    'Flip Monster': False,
    'Flip Effect Monster': False,
    'Flip Tuner Effect Monster': False,
    'Spirit Monster': False,
    'Union Effect Monster': False,
    'Gemini Monster': False,
    'Pendulum Effect Monster': False,
    'Pendulum Normal Monster': False,
    'Pendulum Tuner Effect Monster': False,
    'Ritual Monster': False,
    'Ritual Effect Monster': False,
    'Toon Monster': False,
    'Pendulum Flip Effect Monster': False,
    'Token': False,
    'Fusion Monster': True,
    'Synchro Monster': True,
    'Synchro Tuner Monster': True,
    'Synchro Pendulum Effect Monster': True,
    'XYZ Monster': True,
    'XYZ Pendulum Effect Monster': True,
    'Link Monster': True,
    'Pendulum Effect Fusion Monster': True
}

# Function to check if card belongs in the extra deck
def is_extra_deck(card):
    """Return True if card belongs in the extra deck."""
    return card_type_to_deck.get(card['type'], False)