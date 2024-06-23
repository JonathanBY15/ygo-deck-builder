from flask import Flask, render_template, request, flash, redirect, session, g
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Deck, Card, DeckCard
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

# Environment libraries
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

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

# Home route
@app.route('/')
def home():
    """Home page."""
    return render_template('home.html')

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
        
        session['username'] = user.username
        flash(f"Welcome {user.username}!", 'success')
        return redirect('/')
    
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login a user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session['username'] = user.username
            flash(f"Welcome back {user.username}!", 'success')
            return redirect('/')
        flash("Invalid credentials", 'danger')
    
    return render_template('login.html', form=form)