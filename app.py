from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Deck, Card, DeckCard
from forms import RegisterForm, LoginForm, UserEditForm, DeckForm, CardSearchForm, RenameDeckForm
from sqlalchemy.exc import IntegrityError
from helpers import fetch_ygo_cards, calculate_card_limit, add_card_to_db, fetch_card_by_id, is_extra_deck


# Environment libraries
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

CURR_USER_KEY = "curr_user"

# Get the database URI and secret key from .env
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# Create and configure app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = False

toolbar = DebugToolbarExtension(app)

# Connect to database
connect_db(app)

# Create tables
with app.app_context():
    db.create_all()

# Create bcrypt instance
bcrypt = Bcrypt(app)



# GLOBAL ERROR HANDLERS
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "An unexpected error occurred"}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    response = {
        "error": "An unexpected error occurred",
        "message": str(error)
    }
    return jsonify(response), 500


# Add user to Flask global
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

# --------------
# --- ROUTES ---
# --------------

# Home route
@app.route('/', methods=['GET', 'POST'])
def homepage():
    """Home page."""

    popular_decks = [
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/88284599.jpg',
        'deck_name': 'voice voi',
        'href': 'https://ygoprodeck.com/deck/voice-voi-512763'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/28143384.jpg',
        'deck_name': 'Yubel Fiendsmith',
        'href': 'https://ygoprodeck.com/deck/yubel-fiendsmith-july-2024-512480'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/73542331.jpg',
        'deck_name': 'Pure Build Kashtira',
        'href': 'https://ygoprodeck.com/deck/pure-build-kashtira-512751'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/27204311.jpg',
        'deck_name': 'Fiendsmith Centur-Ion',
        'href': 'https://ygoprodeck.com/deck/fiendsmith-centur-ion-july-2024-512714'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/93860227.jpg',
        'deck_name': 'Voiceless Voice Fiendsmith Tune',
        'href': 'https://ygoprodeck.com/deck/voiceless-voice-fiendsmith-tune-512705'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/96030710.jpg',
        'deck_name': 'Centur-Ion',
        'href': 'https://ygoprodeck.com/deck/centur-ion-july-2024-512626'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/91810826.jpg',
        'deck_name': 'Tenpai deck',
        'href': 'https://ygoprodeck.com/deck/tenpai-deck-512615'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/10000020.jpg',
        'deck_name': 'Osiris - The Sky Dragon',
        'href': 'https://ygoprodeck.com/deck/osiris-the-sky-dragon-512609'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/53842431.jpg',
        'deck_name': 'Trif',
        'href': 'https://ygoprodeck.com/deck/trif-512603'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/44822037.jpg',
        'deck_name': 'White Wood v 6.0',
        'href': 'https://ygoprodeck.com/deck/white-wood-v-6-0-512598'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/23657016.jpg',
        'deck_name': 'Tenpai Dragon',
        'href': 'https://ygoprodeck.com/deck/tenpai-dragon-512591'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/37617348.jpg',
        'deck_name': 'Rescue-ACE Fiendsmith',
        'href': 'https://ygoprodeck.com/deck/rescue-ace-fiendsmith-512583'
    }
]



    if g.user:
        return render_template('home.html', user=g.user, decks=g.user.decks, popular_decks=popular_decks)
    
    else:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)
            if user:
                session[CURR_USER_KEY] = user.id
                # flash(f"Welcome back {user.username}!", 'success')
                return redirect('/')
            flash("Invalid credentials", 'danger')

        return render_template('/home-anon.html', popular_decks=popular_decks)
    


# Decks route
@app.route('/decks', methods=['GET', 'POST'])
def decks_view():
    """User decks page."""
    if g.user:
        return render_template('decks.html', user=g.user, decks=g.user.decks)
    
    else:
        popular_decks = [
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/88284599.jpg',
        'deck_name': 'voice voi',
        'href': 'https://ygoprodeck.com/deck/voice-voi-512763'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/28143384.jpg',
        'deck_name': 'Yubel Fiendsmith',
        'href': 'https://ygoprodeck.com/deck/yubel-fiendsmith-july-2024-512480'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/73542331.jpg',
        'deck_name': 'Pure Build Kashtira',
        'href': 'https://ygoprodeck.com/deck/pure-build-kashtira-512751'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/27204311.jpg',
        'deck_name': 'Fiendsmith Centur-Ion',
        'href': 'https://ygoprodeck.com/deck/fiendsmith-centur-ion-july-2024-512714'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/93860227.jpg',
        'deck_name': 'Voiceless Voice Fiendsmith Tune',
        'href': 'https://ygoprodeck.com/deck/voiceless-voice-fiendsmith-tune-512705'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/96030710.jpg',
        'deck_name': 'Centur-Ion',
        'href': 'https://ygoprodeck.com/deck/centur-ion-july-2024-512626'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/91810826.jpg',
        'deck_name': 'Tenpai deck',
        'href': 'https://ygoprodeck.com/deck/tenpai-deck-512615'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/10000020.jpg',
        'deck_name': 'Osiris - The Sky Dragon',
        'href': 'https://ygoprodeck.com/deck/osiris-the-sky-dragon-512609'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/53842431.jpg',
        'deck_name': 'Trif',
        'href': 'https://ygoprodeck.com/deck/trif-512603'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/44822037.jpg',
        'deck_name': 'White Wood v 6.0',
        'href': 'https://ygoprodeck.com/deck/white-wood-v-6-0-512598'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/23657016.jpg',
        'deck_name': 'Tenpai Dragon',
        'href': 'https://ygoprodeck.com/deck/tenpai-dragon-512591'
    },
    {
        'image_url': 'https://images.ygoprodeck.com/images/cards_small/37617348.jpg',
        'deck_name': 'Rescue-ACE Fiendsmith',
        'href': 'https://ygoprodeck.com/deck/rescue-ace-fiendsmith-512583'
    }
]

        return render_template('/home-anon.html', popular_decks=popular_decks)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user."""

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.register(form.username.data, form.password.data, form.email.data)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)
        
        session[CURR_USER_KEY] = user.id
        # flash(f"Welcome {user.username}!", 'success')
        return redirect('/')
    
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login a user."""
    form = LoginForm()
    if form.validate_on_submit():
        # Authenticate user
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            # Add user to session and redirect to home
            session[CURR_USER_KEY] = user.id
            # flash(f"Welcome back {user.username}!", 'success')
            return redirect('/')
        
        flash("Invalid credentials", 'danger')
    
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logout a user."""

    if CURR_USER_KEY in session:
        # Remove user from session, if it exists and redirect to home
        del session[CURR_USER_KEY]
        # flash("You have successfully logged out.", "success")
        return redirect("/")
    else:
        # If no user is logged in, flash message and redirect to home
        flash("You are not logged in.", "danger")
        return redirect("/")

# Edit user profile route
@app.route('/user/edit', methods=['GET', 'POST'])
def edit_user():
    """Edit user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = UserEditForm(obj=g.user, user_id=g.user.id)

    if form.validate_on_submit():
        # Authenticate user
        if User.authenticate(g.user.username, form.password.data):
            # Update user and commit changes
            g.user.username = form.username.data
            g.user.email = form.email.data
            g.user.img_url = form.img_url.data

            db.session.commit()
            flash("You successfully updated your profile.", "success")
            return redirect("/")
        
        flash("Invalid credentials.", "danger")

    return render_template('user-edit.html', form=form, user=g.user)

# Add deck route
@app.route('/decks/new', methods=['GET', 'POST'])
def add_deck():
    """Add a deck."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = DeckForm()

    if form.validate_on_submit():
        deck = Deck(user_id=g.user.id, name=form.name.data, description=form.description.data)
        db.session.add(deck)
        db.session.commit()
        return redirect(f"/decks/{deck.id}")
    
    return render_template('deck-add.html', form=form, user=g.user)

# Deck edit route
@app.route('/decks/<int:deck_id>', methods=['GET', 'POST'])
def edit_deck(deck_id):
    """View and edit a deck."""

    deck = Deck.query.get_or_404(deck_id)

    form = CardSearchForm()
    renameDeckForm = RenameDeckForm()
    offset = request.args.get('offset', 0, type=int)
    per_page = 24  # Number of cards per page

    if form.validate_on_submit() or request.method == 'GET':

        # Preserve form data if available
        if not form.validate_on_submit():
            form.name.data = request.args.get('name', '')
            form.type.data = request.args.get('type', '')
            form.attribute.data = request.args.get('attribute', '')
            form.race.data = request.args.get('race', '')
            form.level.data = request.args.get('level', '')
            form.attack.data = request.args.get('attack', '')
            form.defense.data = request.args.get('defense', '')

        cards_data = fetch_ygo_cards(
            fname=form.name.data,
            type=form.type.data if form.type.data != '' else None,
            attribute=form.attribute.data if form.attribute.data != '' else None,
            race=form.race.data if form.race.data != '' else None,
            level=form.level.data if form.level.data != '' else None,
            attack=f"gte{form.attack.data}" if form.attack.data != '' else None,
            defense=f"gte{form.defense.data}" if form.defense.data != '' else None,
            num=per_page,
            offset=offset
        )

        if not cards_data:
            flash("No cards found that fit the filters", "danger")
            return render_template('deck-view.html', deck=deck, form=form, cards=[], offset=offset, renameDeckForm=renameDeckForm, user=g.user)

        # Extract relevant data for rendering
        cards = cards_data['data']
        pages_remaining = cards_data['meta']['pages_remaining']

        return render_template('deck-view.html', deck=deck, cards=cards, form=form, offset=offset, pages_remaining=pages_remaining, renameDeckForm=renameDeckForm, user=g.user)

    return render_template('deck-view.html', deck=deck, form=form, cards=[], offset=0, renameDeckForm=renameDeckForm, user=g.user)


# New Search route for edit deck
@app.route('/decks/<int:deck_id>/cards/new_search', methods=['POST'])
def new_search(deck_id):
    """Called when a new search is made. Resets offset to 0 and redirects to edit_deck with form data."""

    # get form data, set offset to 0, and redirect to edit_deck
    form_data = request.form.to_dict()
    return redirect(url_for('edit_deck', deck_id=deck_id, offset=0, **form_data))


# Previous card page route for deck edit
@app.route('/decks/<int:deck_id>/cards/previous_page', methods=['POST'])
def previous_page(deck_id):
    """Load the previous page of cards."""

    offset = int(request.form['offset'])
    new_offset = max(0, offset - 30)

    # Convert form data to dictionary and remove offset
    form_data = request.form.to_dict()
    form_data.pop('offset', None)
    
    return redirect(url_for('edit_deck', deck_id=deck_id, offset=new_offset, **form_data))

# Next card page route for deck edit
@app.route('/decks/<int:deck_id>/cards/next_page', methods=['POST'])
def next_page(deck_id):
    """Load the next page of cards."""

    offset = int(request.form['offset'])
    new_offset = offset + 30

    # Convert form data to dictionary and remove offset
    form_data = request.form.to_dict()
    form_data.pop('offset', None)
    
    return redirect(url_for('edit_deck', deck_id=deck_id, offset=new_offset, **form_data))

# Delete deck route
@app.route('/decks/<int:deck_id>/delete', methods=['GET', 'POST'])
def delete_deck(deck_id):
    """Delete a deck."""

    deck = Deck.query.get_or_404(deck_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    db.session.delete(deck)
    db.session.commit()
    # flash("Deck deleted.", "success")
    return redirect("/decks")


# Add card to deck route
@app.route('/decks/<int:deck_id>/cards/add/<int:card_id>', methods=['POST'])
def add_card_to_deck(deck_id, card_id):
    """Add one card to a deck. If the user wants to add multiple copies of a card, 
    they can do so by adding the card multiple times. Don't allow the user to add 
    more than limit copies of a card to a deck. CardSearchForm fields should be preserved 
    in the form."""

    if not g.user:
        return jsonify({"error": "Access unauthorized."}), 401

    deck = Deck.query.get_or_404(deck_id)
    card = fetch_card_by_id(card_id)

    if not card:
        return jsonify({"error": "Card not found."}), 404

    card = add_card_to_db(card)

    # If there are more than 60 cards with card.extra_deck = False, don't allow the user to add more cards
    if (not card.extra_deck) and (deck.main_deck_count >= 60):
        return jsonify({"error": "Cannot add more than 60 cards to the main deck."}), 400


    # If there are more than 15 cards with card.extra_deck = True, don't allow the user to add more cards
    if card.extra_deck and (deck.extra_deck_count >= 15):
        return jsonify({"error": "Cannot add more than 15 cards to the extra deck."}), 400
    


    if card.limit == 0:
        return jsonify({"error": f"{card.name} is banned."}), 400

    deck_card = DeckCard.query.filter_by(deck_id=deck_id, card_id=card_id).first()

    if deck_card:
        if deck_card.quantity >= card.limit:
            return jsonify({"error": f"Cannot add more than {card.limit} copies of {card.name}."}), 400
        deck_card.quantity += 1
    else:
        deck_card = DeckCard(deck_id=deck_id, card_id=card.id, quantity=1)
        db.session.add(deck_card)

    db.session.commit()
    return jsonify({"message": f"{card.name} added to {deck.name}."}), 200


# Remove card from deck route
@app.route('/decks/<int:deck_id>/cards/remove/<int:card_id>', methods=['POST'])
def remove_card_from_deck(deck_id, card_id):
    """Remove one card from a deck. If the user wants to remove multiple copies of a card, 
    they can do so by removing the card multiple times. CardSearchForm fields should be 
    preserved in the form."""

    if not g.user:
        return jsonify({"error": "Access unauthorized."}), 401

    deck = Deck.query.get_or_404(deck_id)
    deck_card = DeckCard.query.filter_by(deck_id=deck_id, card_id=card_id).first()
    card = fetch_card_by_id(card_id)

    if not card:
        return jsonify({"error": "Card not found."}), 404

    card = add_card_to_db(card)
    if deck_card:
        deck_card.quantity -= 1
        if deck_card.quantity == 0:
            db.session.delete(deck_card)
        db.session.commit()
        return jsonify({"message": f"{card.name} removed from {deck.name}."}), 200
    return jsonify({"error": f"{card.name} is not in the deck."}), 400


# Clear deck route
@app.route('/decks/<int:deck_id>/clear', methods=['GET', 'POST'])
def clear_deck(deck_id):
    """Clear a deck of all cards."""

    # Check if user is logged in
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    deck = Deck.query.get_or_404(deck_id)

    # Select all deck_cards from database
    deck_cards = DeckCard.query.filter_by(deck_id=deck_id).all()

    # Delete all deck_cards and commit changes
    for deck_card in deck_cards:
        db.session.delete(deck_card)
    db.session.commit()
    
    # flash(f"{deck.name} cleared.", "success")
    return redirect(f"/decks/{deck_id}")



# API ENDPOINTS

# API endpoint to get all cards in a deck
@app.route('/api/decks/<int:deck_id>/cards', methods=['GET'])
def get_deck_cards(deck_id):
    """API endpoint to get all cards in a deck."""

    deck = Deck.query.get_or_404(deck_id)
    cards = [{'id': dc.card_id, 'quantity': dc.quantity, 'is_extra_deck': dc.card.extra_deck, 'img_url': dc.card.img_url, 'card_desc': dc.card.description} for dc in deck.deck_cards]
    return jsonify(cards)

# API endpoint to clear a deck
@app.route('/api/decks/<int:deck_id>/clear', methods=['POST'])
def clear_deck_api(deck_id):
    """API endpoint to clear a deck of all cards."""

    deck = Deck.query.get_or_404(deck_id)
    deck_cards = DeckCard.query.filter_by(deck_id=deck_id).all()

    for deck_card in deck_cards:
        db.session.delete(deck_card)
    db.session.commit()

    return jsonify({"message": f"{deck.name} cleared."})

# API endpoint to search for cards
@app.route('/api/cards/search', methods=['GET', 'POST'])
def search_cards():
    """API endpoint to search for cards."""
    form = CardSearchForm()
    per_page = 30

    # Retrieve offset from request (POST for search form, GET for pagination)
    if request.method == 'POST':
        offset = int(request.form.get('offset', 0))
    else:
        offset = int(request.args.get('offset', 0))

    if form.validate_on_submit() or request.method in ['POST', 'GET']:
        # Preserve form data if available
        if request.method == 'GET' or not form.validate_on_submit():
            form.name.data = request.values.get('name', '')
            form.type.data = request.values.get('type', '')
            form.attribute.data = request.values.get('attribute', '')
            form.race.data = request.values.get('race', '')
            form.level.data = request.values.get('level', '')
            form.attack.data = request.values.get('attack', '')
            form.defense.data = request.values.get('defense', '')
            form.offset.data = offset

        cards_data = fetch_ygo_cards(
            fname=form.name.data,
            type=form.type.data if form.type.data != '' else None,
            attribute=form.attribute.data if form.attribute.data != '' else None,
            race=form.race.data if form.race.data != '' else None,
            level=form.level.data if form.level.data != '' else None,
            attack=f"gte{form.attack.data}" if form.attack.data != '' else None,
            defense=f"gte{form.defense.data}" if form.defense.data != '' else None,
            num=per_page,
            offset=offset
        )

        if not cards_data:
            return jsonify({"error": "No cards found that fit the filters."}), 404

        # Extract relevant data for rendering
        cards = cards_data['data']
        pages_remaining = cards_data['meta']['pages_remaining']

        return jsonify({"cards": cards, "offset": offset, "pages_remaining": pages_remaining})

    return jsonify({"error": "Invalid form data."}), 400

# API endpoint to rename a deck
@app.route('/api/<int:deck_id>/rename', methods=['POST'])
def rename_deck(deck_id):
    """API endpoint to rename a deck."""
    deck = Deck.query.get_or_404(deck_id)

    # Check if user is logged in
    if not g.user:
        return jsonify({"error": "Access unauthorized."}), 401

    form = RenameDeckForm()

    if form.validate_on_submit():
        deck.name = form.name.data
        db.session.commit()
        return redirect(f"/decks/{deck_id}")

    return jsonify({"error": "Invalid form data."}), 400

# API endpoint to set a decks cover image
@app.route('/api/<int:deck_id>/set_cover/<int:card_id>', methods=['GET', 'POST'])
def set_deck_cover(deck_id, card_id):
    """API endpoint to set a decks cover image."""
    deck = Deck.query.get_or_404(deck_id)
    card = fetch_card_by_id(card_id)

    if not card:
        return jsonify({"error": "Card not found."}), 404

    deck.cover_card_url = card['card_images'][0]['image_url_small']
    db.session.commit()
    return jsonify({"message": f"Cover image set to {card['name']}."}), 200

