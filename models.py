"""SQLAlchemy models for YGO Deck Builder."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    hash_password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    img_url = db.Column(db.String, nullable=False, default="/static/images/user_vesikalik.png")

    # Relationships
    decks = db.relationship("Deck", back_populates="user", cascade="all, delete-orphan")

    # Methods
    @classmethod
    def register(cls, username, unhash_password, email):
        """Register user with hashed password, return user."""
        hashed = bcrypt.generate_password_hash(unhash_password).decode("utf8")
        user = cls(username=username, hash_password=hashed, email=email)
        # db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, unhash_password):
        """Validate that user exists & password is correct.
        Return user if valid; else return False."""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.hash_password, unhash_password):
            return user
        return False

class Deck(db.Model):
    """A deck."""

    __tablename__ = "decks"

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=True)

    # Relationships
    user = db.relationship("User", back_populates="decks")
    deck_cards = db.relationship("DeckCard", back_populates="deck", cascade="all, delete-orphan")
    cover_card = db.relationship("Card", foreign_keys=[cover_card_id], uselist=False)

    # Methods
    @validates('cover_card_id')
    def validate_cover_card(self, key, cover_card_id):
        """Validate that cover card is in the deck."""
        if cover_card_id is not None:
            card_ids_in_deck = [deck_card.card_id for deck_card in self.deck_cards]
            if cover_card_id not in card_ids_in_deck:
                raise ValueError("Cover card must be one of the cards in the deck.")
        return cover_card_id

class Card(db.Model):
    """A card."""

    __tablename__ = "cards"

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    attribute = db.Column(db.String(50), nullable=True)
    race = db.Column(db.String(50), nullable=True)
    level = db.Column(db.Integer, nullable=True)
    attack = db.Column(db.Integer, nullable=True)
    defense = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    img_url = db.Column(db.String, nullable=False)
    limit = db.Column(db.Integer, nullable=False, default=3)

    # Relationships
    deck_cards = db.relationship("DeckCard", back_populates="card", cascade="all, delete-orphan")

class DeckCard(db.Model):
    """A card in a deck."""

    __tablename__ = "deck_cards"

    # Columns
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # Relationships
    deck = db.relationship("Deck", back_populates="deck_cards")
    card = db.relationship("Card", back_populates="deck_cards")

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        """Validate that quantity does not exceed card limit"""
        if self.card is None:
            card = Card.query.get(self.card_id)
        else:
            card = self.card
        if card is None:
            raise ValueError("Card does not exist.")
        if quantity > card.limit or quantity > 3 or quantity < 0:
            raise ValueError(f"Invalid quantity. {card.name} quantity must be between 0 and {min(card.limit, 3)}.")
        return quantity


# Function to connect to the database
def connect_db(app):
    """Connect this database to provided Flask app.
    Call this in your Flask app.py to connect the database to the Flask app."""
    db.app = app
    db.init_app(app)
