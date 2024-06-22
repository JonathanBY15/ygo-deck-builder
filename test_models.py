import unittest
from flask import Flask
from models import db, User, Deck, Card, DeckCard
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Replace with your actual database URI
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test database and create tables."""
        # Create a minimal Flask application
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.config['TESTING'] = True

        # Initialize the database with the Flask app
        db.init_app(cls.app)

        # Create the test database and tables
        with cls.app.app_context():
            db.drop_all()  # Drop all tables to ensure a clean slate
            db.create_all()
            cls.create_test_data()

    @classmethod
    def create_test_data(cls):
        """Create test data."""
        # Create some test users
        user1 = User.register(username="testuser1", unhash_password="password", email="test1@test.com")
        user2 = User.register(username="testuser2", unhash_password="password", email="test2@test.com")

        # Add users to the session
        db.session.add(user1)
        db.session.add(user2)

        # Create some test cards
        card1 = Card(name="Card 1", type="Monster", img_url="http://example.com/card1.jpg")
        card2 = Card(name="Card 2", type="Spell", img_url="http://example.com/card2.jpg")
        card3 = Card(name="Card 3", type="Trap", img_url="http://example.com/card3.jpg")

        # Add cards to the session
        db.session.add(card1)
        db.session.add(card2)
        db.session.add(card3)

        # Commit the session to save the data to the database
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database."""
        with cls.app.app_context():
            db.drop_all()

    def test_user_registration(self):
        """Test user registration."""
        with self.app.app_context():
            user = User.query.filter_by(username="testuser1").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test1@test.com")

    def test_card_creation(self):
        """Test card creation."""
        with self.app.app_context():
            card = Card.query.filter_by(name="Card 1").first()
            self.assertIsNotNone(card)
            self.assertEqual(card.type, "Monster")


