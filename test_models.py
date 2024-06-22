import unittest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import User, Deck, Card, DeckCard

# Load environment variables
load_dotenv()

# Replace with your actual database URI
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# Create a Flask application factory
def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications for better performance
    return app

# Initialize Flask app, SQLAlchemy, and Bcrypt
app = create_app()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Create an engine to connect to the database and a session to communicate with the database
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the testing environment."""
        # Push an application context
        cls.app_context = app.app_context()
        cls.app_context.push()

        # Initialize database session
        cls.session = Session()

        # Create tables (if not exist)
        db.create_all()

        # Create test data
        cls.create_test_data()

    @classmethod
    def tearDownClass(cls):
        """Tear down the testing environment."""
        # Remove test data
        db.session.remove()
        db.drop_all()

        # Pop the application context
        cls.app_context.pop()

    @classmethod
    def create_test_data(cls):
        """Create test data for the tests."""
        # Create some test users
        user1 = User.register(username='user1', unhash_password='password1', email='user1@example.com')
        user2 = User.register(username='user2', unhash_password='password2', email='user2@example.com')

        # Create some decks for user1
        deck1 = Deck(name='Deck 1', user=user1)
        deck2 = Deck(name='Deck 2', user=user1)

        # Add cards and deck cards (assuming you have Card and DeckCard models defined)
        card1 = Card(name='Card 1', type='Monster')
        card2 = Card(name='Card 2', type='Spell')
        card3 = Card(name='Card 3', type='Trap')

        deck_card1 = DeckCard(deck=deck1, card=card1, quantity=3)
        deck_card2 = DeckCard(deck=deck2, card=card2, quantity=2)
        deck_card3 = DeckCard(deck=deck2, card=card3, quantity=1)

        # Add objects to the session only if they are not already attached
        for obj in [user1, user2, deck1, deck2, card1, card2, card3, deck_card1, deck_card2, deck_card3]:
            if obj not in cls.session:
                cls.session.add(obj)

        # Commit all changes to the database
        cls.session.commit()



    def test_create_user(self):
        """Test creating a new user."""
        user = User(username='testuser', password='password', email='test@example.com')
        self.session.add(user)
        self.session.commit()

        # Check that the user was added to the database
        self.assertIsNotNone(user.id)

    def test_delete_user_cascades_decks(self):
        """Test deleting a user cascades to delete associated decks."""
        # Get user1 and its decks
        user1 = self.session.query(User).filter_by(username='user1').first()
        self.assertIsNotNone(user1)

        num_decks_before_delete = self.session.query(Deck).filter_by(user_id=user1.id).count()

        # Delete user1
        self.session.delete(user1)
        self.session.commit()

        # Check that user1 and its decks are deleted
        deleted_user1 = self.session.query(User).filter_by(username='user1').first()
        num_decks_after_delete = self.session.query(Deck).filter_by(user_id=user1.id).count()

        self.assertIsNone(deleted_user1)
        self.assertEqual(num_decks_after_delete, 0)

    # Additional tests for update, read, delete operations can be added similarly