from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
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