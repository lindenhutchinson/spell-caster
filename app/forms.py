from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])

    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    """Register user form."""
    username = StringField('Name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    """Login user form."""
    username = StringField('Name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Submit')

class CharacterForm(FlaskForm):
    """Create character form."""
   
    name = StringField('Name', [DataRequired()])
    race = StringField('Race', [DataRequired()])
    level = IntegerField('Level', [DataRequired()])
    saving_throw = StringField('Saving Throw', [DataRequired()])
    ability_score = IntegerField('Ability Score', [DataRequired()])

    class_id = SelectField(u'Class')
    submit = SubmitField('Submit')

class PickCharacterForm(FlaskForm):
    """Select your character."""

    character = SelectField(u'Character')
    submit = SubmitField('Select')
