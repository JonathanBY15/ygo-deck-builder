from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class RegisterForm(FlaskForm):
    """Form for registering a user."""
    
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_password_confirm(self, password_confirm):
        """Validate that password_confirm matches password."""
        if password_confirm.data != self.password.data:
            raise ValidationError('Passwords must match')
        
    def validate_username(self, username):
        """Validate that username is unique."""
        from models import User
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already taken')
        
    def validate_email(self, email):
        """Validate that email is unique."""
        from models import User
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already taken')
        
class LoginForm(FlaskForm):
    """Form for logging in a user."""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, username):
        """Validate that username exists."""
        from models import User
        if not User.query.filter_by(username=username.data).first():
            raise ValidationError('Username not found')
        
    def validate_password(self, password):
        """Validate that password is correct."""
        from models import User
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.authenticate(self.username.data, password.data):
            raise ValidationError('Invalid password')
        
class UserEditForm(FlaskForm):
    """Form for editing a user."""
    
    username = StringField('Username', validators=[Length(min=3, max=20)])
    email = StringField('Email', validators=[Email()])
    image_url = StringField('Image URL')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])

    def __init__(self, *args, **kwargs):
        """Override init to accept user_id."""
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
    
    def validate_password_confirm(self, password_confirm):
        """Validate that password_confirm matches password."""
        if password_confirm.data != self.password.data:
            raise ValidationError('Passwords must match')
        
    def validate_username(self, username):
        """Validate that username is unique."""
        from models import User
        user = User.query.filter_by(username=username.data).first()
        if user and user.id != self.user_id:
            raise ValidationError('Username already taken')
        
    def validate_email(self, email):
        """Validate that email is unique."""
        from models import User
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != self.user_id:
            raise ValidationError('Email already taken')
        
class DeckForm(FlaskForm):
    """Form for adding a deck."""
    
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Description')
    
    # def validate_cover_card_id(self, cover_card_id):
    #     """Validate that cover card is in the deck."""
    #     from models import Card
    #     if cover_card_id.data:
    #         card = Card.query.get(cover_card_id.data)
    #         if not card:
    #             raise ValidationError('Cover card not found')

class CardSearchForm(FlaskForm):
    """Form for searching for cards."""
    
    name = StringField('Name')
    type = SelectField('Type', choices=[
        ('', 'Card Type'),
        ('Skill Card', 'Skill Card'), 
        ('Spell Card', 'Spell Card'), 
        ('Trap Card', 'Trap Card'), 
        ('Normal Monster', 'Normal Monster'), 
        ('Normal Tuner Monster', 'Normal Tuner Monster'), 
        ('Effect Monster', 'Effect Monster'), 
        ('Tuner Monster', 'Tuner Monster'), 
        ('Flip Effect Monster', 'Flip Effect Monster'), 
        ('Flip Tuner Effect Monster', 'Flip Tuner Effect Monster'), 
        ('Spirit Monster', 'Spirit Monster'), 
        ('Union Effect Monster', 'Union Effect Monster'), 
        ('Gemini Monster', 'Gemini Monster'), 
        ('Pendulum Effect Monster', 'Pendulum Effect Monster'), 
        ('Pendulum Normal Monster', 'Pendulum Normal Monster'), 
        ('Pendulum Tuner Effect Monster', 'Pendulum Tuner Effect Monster'), 
        ('Ritual Monster', 'Ritual Monster'), 
        ('Ritual Effect Monster', 'Ritual Effect Monster'), 
        ('Toon Monster', 'Toon Monster'), 
        ('Fusion Monster', 'Fusion Monster'), 
        ('Synchro Monster', 'Synchro Monster'), 
        ('Synchro Tuner Monster', 'Synchro Tuner Monster'), 
        ('Synchro Pendulum Effect Monster', 'Synchro Pendulum Effect Monster'), 
        ('XYZ Monster', 'XYZ Monster'), 
        ('XYZ Pendulum Effect Monster', 'XYZ Pendulum Effect Monster'), 
        ('Link Monster', 'Link Monster'), 
        ('Pendulum Flip Effect Monster', 'Pendulum Flip Effect Monster'), 
        ('Pendulum Effect Fusion Monster', 'Pendulum Effect Fusion Monster'), 
        ('Token', 'Token')
    ])
    attribute = SelectField('Attribute', choices=[
        ('', 'Attribute'),
        ('dark', 'Dark'), 
        ('earth', 'Earth'), 
        ('fire', 'Fire'), 
        ('light', 'Light'), 
        ('water', 'Water'), 
        ('wind', 'Wind'), 
        ('divine', 'Divine')
    ])
    race = SelectField('Race', choices=[
        ('', 'Race'),
        ('continuous', 'Continuous'),
        ('zombie', 'Zombie'),
        ('fiend', 'Fiend'),
        ('normal', 'Normal'),
        ('quick-play', 'Quick-Play'),
        ('rock', 'Rock'),
        ('warrior', 'Warrior'),
        ('winged beast', 'Winged Beast'),
        ('spellcaster', 'Spellcaster'),
        ('beast', 'Beast'),
        ('fairy', 'Fairy'),
        ('equip', 'Equip'),
        ('field', 'Field'),
        ('fish', 'Fish'),
        ('beast-warrior', 'Beast-Warrior'),
        ('thunder', 'Thunder'),
        ('machine', 'Machine'),
        ('sea serpent', 'Sea Serpent'),
        ('aqua', 'Aqua'),
        ('plant', 'Plant'),
        ('dragon', 'Dragon'),
        ('reptile', 'Reptile'),
        ('counter', 'Counter'),
        ('psychic', 'Psychic'),
        ('insect', 'Insect'),
        ('pyro', 'Pyro'),
        ('dinosaur', 'Dinosaur'),
        ('wyrm', 'Wyrm'),
        ('cyberse', 'Cyberse'),
        ('illusion', 'Illusion'),
        ('ritual', 'Ritual'),
        ('divine-beast', 'Divine-Beast'),
        ('creator-god', 'Creator-God'),
        ('cyverse', 'Cyverse'),
        ('mai', 'Mai'),
        ('pegasus', 'Pegasus'),
        ('ishizu', 'Ishizu'),
        ('joey', 'Joey'),
        ('kaiba', 'Kaiba'),
        ('yugi', 'Yugi')
    ])
    level = SelectField('Level', choices=[
        ('', 'Level'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12')
    ])
    attack = StringField('ATK')
    defense = StringField('DEF')
    offset = HiddenField('Offset', default=0)

