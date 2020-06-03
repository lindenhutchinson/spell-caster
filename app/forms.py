from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField, SelectField, StringField, TextField, TextAreaField, SubmitField, PasswordField, BooleanField, IntegerField
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
    submit = SubmitField('Save')


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
    submit = SubmitField('Save')

class PickNoteForm(FlaskForm):
    """Select a note form."""

    note_id = SelectField(u'Notes')
    submit = SubmitField('Select')

class NoteForm(FlaskForm):
    """A General Notes Form""" 
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Your thoughts...', [DataRequired()])
    submit = SubmitField('Save')



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PickSpellForm(FlaskForm):
    submit = SubmitField('Save')
    spell_ids = MultiCheckboxField('Spells')

class SpellForm(FlaskForm):
    """Spell form."""

    name = StringField('Name', [DataRequired()])
    level = IntegerField("Level", [DataRequired()])
    cast_time = StringField("Cast time", [DataRequired()])
    spell_range = StringField("Range", [DataRequired()])
    components = StringField("Components", [DataRequired()])
    duration = StringField("Duration", [DataRequired()])
    school = StringField("School", [DataRequired()])
    info = TextAreaField("Description", [DataRequired()])
    scaling = BooleanField("What does this spell do at higher levels?")
    from_book = StringField("What's your source?")
    concentration = BooleanField("Requires Concentration")
    is_bard = BooleanField("Bard")
    is_cleric = BooleanField("Cleric")
    is_druid = BooleanField("Druid")
    is_paladin = BooleanField("Paladin")
    is_ranger = BooleanField("Ranger")
    is_sorcerer = BooleanField("Sorcerer")
    is_warlock = BooleanField("Warlock")
    is_wizard = BooleanField("Wizard")
    submit = SubmitField('Save')

