from flask import Flask, render_template, request, flash, redirect, session, g
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Deck, Card, DeckCard
from forms import RegisterForm, LoginForm, UserEditForm, DeckForm, CardSearchForm
from sqlalchemy.exc import IntegrityError
from helpers import fetch_ygo_cards
import requests

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

# Deck edit route
@app.route('/decks/<int:deck_id>')
def show_deck(deck_id):
    """Show a deck."""

    deck = Deck.query.get_or_404(deck_id)
    return render_template('deck-view.html', deck=deck)

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




# TODO: Implement the following functions (then move it to a separate file)

# Function to calculate card limit
def calculate_card_limit(card):
    """Calculate the card limit."""

# Function to add card to database
def add_card_to_db(card):
    """Add a card to the database."""
    



@app.route('/cards', methods=['GET', 'POST'])
def get_cards():
    """Get card images. Search for cards by name and display images."""
    form = CardSearchForm()

    if form.validate_on_submit():
        cards_data = fetch_ygo_cards(fname=form.name.data, 
                                     type=form.type.data if form.type.data != '' else None, 
                                     attribute=form.attribute.data if form.attribute.data != '' else None, 
                                     race=form.race.data if form.race.data != '' else None, 
                                     level=form.level.data if form.level.data != '' else None, 
                                     attack=f"gte{form.attack.data}" if form.attack.data != '' else None, 
                                     defense=f"gte{form.defense.data}" if form.defense.data != '' else None)
        if not cards_data:
            return "Error fetching card data", 500
        
        return render_template('cards.html', cards=cards_data, form=form)
    
    return render_template('cards.html', form=form)
