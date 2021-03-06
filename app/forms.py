from flask_wtf import FlaskForm
from wtforms import widgets, FormField, SelectMultipleField, SelectField, StringField, TextField, TextAreaField, SubmitField, PasswordField, BooleanField, IntegerField
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

class StatsForm(FlaskForm):
    str_ = IntegerField("Strength")
    con_ = IntegerField("Constitution")
    dex_ = IntegerField("Dexterity")
    wis_ = IntegerField("Wisdom")
    int_ = IntegerField("Intelligence")
    chr_ = IntegerField("Charisma")
    ac = IntegerField("Armour Class")
    max_hp = IntegerField("Hit Point Maximum")
    spell_save = IntegerField("Spell Save DC")
    spell_attack = IntegerField("Spell Attack Modifier")
    submit = SubmitField('Save')

class CharacterForm(FlaskForm):
    """Create character form."""
    
    name = StringField('Name', [DataRequired()])
    level = IntegerField('Level', [DataRequired()])
    class_id = SelectField(u'Class')
    is_npc = BooleanField('This is an NPC')
    submit = SubmitField('Save')


class PickCharacterForm(FlaskForm):
    """Select a character form."""

    character = SelectField(u'Characters')
    submit = SubmitField('Select')

class ActionForm(FlaskForm):
    """Create an action form """
    name = StringField('Name')
    desc = TextAreaField('Description')
    max_res = IntegerField('How many times can you use this?')
    submit = SubmitField('Save')

class PickActionForm(FlaskForm):
    """Select an action form."""

    id = SelectField(u'Actions')
    submit = SubmitField('Select')



class PickClassForm(FlaskForm):
    """Select a class form."""

    class_id = SelectField(u'Classes')
    submit = SubmitField('Select')


class ClassForm(FlaskForm):
    """Create class form."""
    submit = SubmitField('Save')
    name = StringField('Name', [DataRequired()])
    desc = TextAreaField('Description', [DataRequired()], render_kw={"rows": 50, "cols": 50})

class PickNoteForm(FlaskForm):
    """Select a note form."""

    note_id = SelectField(u'Notes')
    submit = SubmitField('Select')

class NoteForm(FlaskForm):
    """A General Notes Form""" 
    submit = SubmitField('Save')
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Your thoughts...', [DataRequired()],render_kw={"rows": 50, "cols": 50})



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PickSpellForm(FlaskForm):
    spell_ids = SelectField(u'Spells')
    submit = SubmitField('Select')

class SpellForm(FlaskForm):
    """Spell form."""

    name = StringField('Name', [DataRequired()])
    level = IntegerField("Level")
    cast_time = StringField("Cast time", [DataRequired()])
    spell_range = StringField("Range", [DataRequired()])
    components = StringField("Components")
    duration = StringField("Duration", [DataRequired()])
    school = StringField("School", [DataRequired()])
    info = TextAreaField("Description", [DataRequired()])
    scaling = StringField("What does this spell do at higher levels?")
    from_book = StringField("What's your source?")
    concentration = BooleanField("Concentration Spell")
    is_bard = BooleanField("Bard")
    is_cleric = BooleanField("Cleric")
    is_druid = BooleanField("Druid")
    is_paladin = BooleanField("Paladin")
    is_ranger = BooleanField("Ranger")
    is_sorcerer = BooleanField("Sorcerer")
    is_warlock = BooleanField("Warlock")
    is_wizard = BooleanField("Wizard")
    submit = SubmitField('Save')


class UnprepareAllForm(FlaskForm):
    submit = SubmitField('Unprepare All Spells')

class ResetSlotsForm(FlaskForm):
    submit = SubmitField('Reset Slots')

class RandomForm(FlaskForm):
    submit = SubmitField('Randomize!')

class DeckForm(FlaskForm):
    name = StringField("Deck name")
    is_com = BooleanField("Commander deck")
    submit = SubmitField('Save')

class PickMPlayerForm(FlaskForm):
    player_id = SelectField("Players")
    submit = SubmitField("Delete")

class PickDeckForm(FlaskForm):
    deck_id = SelectField("Decks")
    submit = SubmitField("Delete")

class MPlayerForm(FlaskForm):
    name = StringField("Name")
    submit = SubmitField('Save')


