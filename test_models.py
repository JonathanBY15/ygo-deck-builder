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

    # --- SETUP AND TEARDOWN METHODS ---
    def setUp(self):
        """Set up the session and create all tables."""
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up the session and drop all tables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    # --- CREATION TESTS ---
    def test_user_registration(self):
        """Test user registration."""
        with self.app.app_context():
            # Register a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Check that the user was added to the database
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@test.com")

    def test_card_creation(self):
        """Test card creation. Card limit should be 3 by default."""
        with self.app.app_context():
            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com")
            db.session.add(card)
            db.session.commit()

            # Check that the card was added to the database
            card = Card.query.filter_by(name="Test Card").first()
            self.assertIsNotNone(card)
            self.assertEqual(card.name, "Test Card")
            self.assertEqual(card.limit, 3)

    def test_deck_creation(self):
        """Test deck creation."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new deck
            deck = Deck(name="Test Deck", user_id=user.id)
            db.session.add(deck)
            db.session.commit()

            # Check that the deck was added to the database
            deck = Deck.query.filter_by(name="Test Deck").first()
            self.assertIsNotNone(deck)
            self.assertEqual(deck.user_id, user.id)

    def test_deck_card_creation(self):
        """Test deck card creation."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new deck
            deck = Deck(name="Test Deck", user_id=user.id)
            db.session.add(deck)
            db.session.commit()

            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com")
            db.session.add(card)
            db.session.commit()

            # Add the card to the deck
            deck_card = DeckCard(deck_id=deck.id, card_id=card.id, quantity=3)
            db.session.add(deck_card)
            db.session.commit()

            # Check that the deck card was added to the database
            deck_card = DeckCard.query.filter_by(deck_id=deck.id, card_id=card.id).first()
            self.assertIsNotNone(deck_card)
            self.assertEqual(deck_card.quantity, 3)


    # --- VALIDATION TESTS ---
    def test_cover_card_validation(self):
        """Test cover card validation. Cover card must be one of the cards in the deck."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new deck
            deck = Deck(name="Test Deck", user_id=user.id)
            db.session.add(deck)
            db.session.commit()

            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com")
            db.session.add(card)
            db.session.commit()

            # Add the card to the deck
            deck_card = DeckCard(deck_id=deck.id, card_id=card.id, quantity=3)
            db.session.add(deck_card)
            db.session.commit()

            # --- POSITIVE TEST CASE ---

            # Set the cover card to the card
            deck.cover_card_id = card.id
            db.session.commit()

            # Check that the cover card was set to the card
            deck = Deck.query.filter_by(name="Test Deck").first()
            self.assertIsNotNone(deck.cover_card_id)
            self.assertEqual(deck.cover_card_id, card.id)
            
            # --- NEGATIVE TEST CASE ---

            # Create a new card (won't add this card to the deck)
            card2 = Card(name="Test Card 2", type="Test Type", img_url="test.com")
            db.session.add(card2)
            db.session.commit()

            # Set the cover card to the card not in the deck and check that the ValueError is raised 
            with self.assertRaises(ValueError):    
                deck.cover_card_id = card2.id
                db.session.commit()

    def test_deck_card_quantity_validation(self):
        """Test deck card quantity. deck_card.quantity shouldn't exceed 3 or card.limit. deck_card.quantity should be at least 1."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new deck
            deck = Deck(name="Test Deck", user_id=user.id)
            db.session.add(deck)
            db.session.commit()

            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com", limit=2)
            db.session.add(card)
            db.session.commit()

            # Add the card to the deck and Check that the Invalid quantity error is raised
            with self.assertRaises(ValueError):
                deck_card = DeckCard(deck_id=deck.id, card_id=card.id, quantity=3)
                db.session.add(deck_card)
                db.session.commit()


    # --- CONSTRAINT TESTS ---
    def test_user_unique_username_constraint(self):
        """Test user unique username constraint."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new user with the same username
            user2 = User.register(username="testuser", unhash_password="password", email="test2@test.com")
            db.session.add(user2)

            # Check that the IntegrityError is raised
            with self.assertRaises(Exception):
                db.session.commit()

    def test_user_unique_email_constraint(self):
        """Test user unique email constraint."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new user with the same email
            user2 = User.register(username="testuser2", unhash_password="password", email="test@test.com")
            db.session.add(user2)

            # Check that the IntegrityError is raised
            with self.assertRaises(Exception):
                db.session.commit()


    # --- DELETION TESTS ---
    def test_card_delete(self):
        """Test card deletion."""
        with self.app.app_context():
            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com", limit=2)
            db.session.add(card)
            db.session.commit()

            # Delete the card
            db.session.delete(card)
            db.session.commit()

            # Check that the card was deleted from the database
            card = Card.query.filter_by(name="Test Card").first()
            self.assertIsNone(card)

    def test_deck_delete(self):
        """Test deck deletion. Deleting a deck should delete all deck cards associated with the deck."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new deck
            deck = Deck(name="Test Deck", user_id=user.id)
            db.session.add(deck)
            db.session.commit()

            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com", limit=2)
            db.session.add(card)
            db.session.commit()

            # Add the card to the deck
            deck_card = DeckCard(deck_id=deck.id, card_id=card.id, quantity=1)
            db.session.add(deck_card)
            db.session.commit()

            # Delete the deck
            db.session.delete(deck)
            db.session.commit()

            # Check that the deck was deleted from the database
            deck = Deck.query.filter_by(name="Test Deck").first()
            self.assertIsNone(deck)

            # Check that the deck card was deleted from the database
            deck_card = DeckCard.query.first()
            self.assertIsNone(deck_card)

    def test_user_delete(self):
        """Test user deletion. Deleting a user should delete all decks associated with the user, and all deck cards associated with the decks."""
        with self.app.app_context():
            # Create a new user
            user = User.register(username="testuser", unhash_password="password", email="test@test.com")
            db.session.add(user)
            db.session.commit()

            # Create a new deck
            deck = Deck(name="Test Deck", user_id=user.id)
            db.session.add(deck)
            db.session.commit()

            # Create a new card
            card = Card(name="Test Card", type="Test Type", img_url="test.com", limit=2)
            db.session.add(card)
            db.session.commit()

            # Add the card to the deck
            deck_card = DeckCard(deck_id=deck.id, card_id=card.id, quantity=1)
            db.session.add(deck_card)
            db.session.commit()

            # Delete the user
            db.session.delete(user)
            db.session.commit()

            # Check that the user was deleted from the database
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNone(user)

            # Check that the deck was deleted from the database
            deck = Deck.query.filter_by(name="Test Deck").first()
            self.assertIsNone(deck)

            # Check that the deck card was deleted from the database
            deck_card = DeckCard.query.first()
            self.assertIsNone(deck_card)


