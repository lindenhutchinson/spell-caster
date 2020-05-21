from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextField,TextAreaField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length

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
    """Select a character form."""

    character = SelectField(u'Characters')
    submit = SubmitField('Select')

class PickClassForm(FlaskForm):
    """Select a class form."""

    class_id = SelectField(u'Classes')
    submit = SubmitField('Select')

class ClassForm(FlaskForm):
    """Create class form."""
    name = StringField('Name', [DataRequired()])
    desc = TextAreaField('Description', [DataRequired()])
    submit = SubmitField('Submit')

