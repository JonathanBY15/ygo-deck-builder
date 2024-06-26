from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Deck, Card, DeckCard
from forms import RegisterForm, LoginForm, UserEditForm, DeckForm, CardSearchForm
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

# Add user to Flask global
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

# Home route
@app.route('/')
def homepage():
    """Home page."""
    if g.user:
        return render_template('home.html', user=g.user, decks=g.user.decks)
    else:
        return render_template('/home-anon.html')

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
        flash(f"Welcome {user.username}!", 'success')
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
            flash(f"Welcome back {user.username}!", 'success')
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
        flash("You have successfully logged out.", "success")
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
            g.user.image_url = form.image_url.data

            db.session.commit()
            flash("You successfully updated your profile.", "success")
            return redirect("/")
        
        flash("Invalid credentials.", "danger")

    return render_template('user-edit.html', form=form)

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
        flash("Deck added.", "success")
        return redirect(f"/decks/{deck.id}")
    
    return render_template('deck-add.html', form=form)


# -------- DECK EDIT ROUTES -----------------------------------------------------------------------------------------------------------

# Deck edit route
@app.route('/decks/<int:deck_id>', methods=['GET', 'POST'])
def edit_deck(deck_id):
    """View and edit a deck."""

    deck = Deck.query.get_or_404(deck_id)

    form = CardSearchForm()
    offset = request.args.get('offset', 0, type=int)
    per_page = 20  # Number of cards per page

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
            return render_template('deck-view.html', deck=deck, form=form, cards=[], offset=offset)

        # Extract relevant data for rendering
        cards = cards_data['data']
        pages_remaining = cards_data['meta']['pages_remaining']

        return render_template('deck-view.html', deck=deck, cards=cards, form=form, offset=offset, pages_remaining=pages_remaining)

    return render_template('deck-view.html', deck=deck, form=form, cards=[], offset=0)


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
    new_offset = max(0, offset - 20)

    # Convert form data to dictionary and remove offset
    form_data = request.form.to_dict()
    form_data.pop('offset', None)
    
    return redirect(url_for('edit_deck', deck_id=deck_id, offset=new_offset, **form_data))

# Next card page route for deck edit
@app.route('/decks/<int:deck_id>/cards/next_page', methods=['POST'])
def next_page(deck_id):
    """Load the next page of cards."""

    offset = int(request.form['offset'])
    new_offset = offset + 20

    # Convert form data to dictionary and remove offset
    form_data = request.form.to_dict()
    form_data.pop('offset', None)
    
    return redirect(url_for('edit_deck', deck_id=deck_id, offset=new_offset, **form_data))

# ------------------------------------------------------------------------------------------------------------------------------------

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
    flash("Deck deleted.", "success")
    return redirect("/")



# Add card to deck route
@app.route('/decks/<int:deck_id>/cards/add/<int:card_id>', methods=['GET', 'POST'])
def add_card_to_deck(deck_id, card_id):
    """Add one card to a deck. If the user wants to add multiple copies of a card, they can do so by adding the card multiple times. Don't allow the user to add more than limit copies of a card to a deck. CardSearchForm fields should be preserved in the form."""

    # Check if user is logged in
    if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")

    deck = Deck.query.get_or_404(deck_id)

    # Fetch card from external database
    card = fetch_card_by_id(card_id)

    # Flash message if card is not found in the API
    if not card:
        flash("Card not found in the external database.", "danger")
        return redirect(request.referrer or "/")
    
    # If card exists, add it to the db
    card = add_card_to_db(card)

    # Check if the card is banned
    if card.limit == 0:
        flash(f"{card.name} is banned and cannot be added to a deck.", "danger")
        return redirect(request.referrer or f"/decks/{deck_id}")

    # Select deck_card from database if it exists
    deck_card = DeckCard.query.filter_by(deck_id=deck_id, card_id=card_id).first()

    # Ceck if card is in deck
    if deck_card:
        if deck_card.quantity >= card.limit:
            # If quantity is greater than or equal to limit, flash message
            flash(f"Cannot add more than {card.limit} copies of {card.name}.", "danger")
        else:
            # Increment quantity and commit changes
            deck_card.quantity += 1
            db.session.commit()
            flash(f"{card.name} added to {deck.name}.", "success")
    else:
        # If card is not in deck, add card to deck
        deck_card = DeckCard(deck_id=deck_id, card_id=card.id, quantity=1)
        db.session.add(deck_card)
        db.session.commit()
        flash(f"{card.name} added to {deck.name}.", "success")

    return redirect(f"/decks/{deck_id}")



# Remove card from deck route
@app.route('/decks/<int:deck_id>/cards/remove/<int:card_id>', methods=['GET', 'POST'])
def remove_card_from_deck(deck_id, card_id):
    """Remove one card from a deck. If the user wants to remove multiple copies of a card, they can do so by removing the card multiple times. CardSearchForm fields should be preserved in the form."""

    # Check if user is logged in
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    deck = Deck.query.get_or_404(deck_id)

    # Select deck_card from database if it exists
    deck_card = DeckCard.query.filter_by(deck_id=deck_id, card_id=card_id).first()

    # Fetch card from external database
    card = fetch_card_by_id(card_id)

    # Flash message if card is not found in the API
    if not card:
        flash("Card not found in the external database.", "danger")
        return redirect(request.referrer or "/")
    
    # If card exists, add it to the db
    card = add_card_to_db(card)

    if deck_card:
        # Decrement quantity and commit changes
        deck_card.quantity -= 1
        db.session.commit()
        flash(f"{card.name} removed from {deck.name}.", "success")

        # If quantity is 0, remove card from deck
        if deck_card.quantity == 0:
            db.session.delete(deck_card)
            db.session.commit()
    
    return redirect(f"/decks/{deck_id}")