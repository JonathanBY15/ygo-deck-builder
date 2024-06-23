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