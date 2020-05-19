from app.models.user import User
from app.models.character import Character
from app.models.spell import Spell
from app.models.spellbook import Spellbook
from app.models._class import _Class
from app.models.subclass import Subclass
from app.models.slots import Slots
from app.db import db


def db_add(o):
    db.db.execute(o)


def add_user(name, password):
    user = User(name, password)
    db_add(user)
    return user

def add_character(name, race, user_id):
    char = Character(name, race, user_id)
    db_add(char)
    return char

def add_spell(name):
    spell = Spell(name)
    db_add(spell)
    return spell

def add_subclass(name, desc, resource_name):
    subclass = Subclass(name, desc, resource_name)
    db_add(subclass)
    return subclass

def add_class(char_id, name, level, desc, saving_throw, subclass_id):
    _class = _Class(char_id, name, level, desc, saving_throw, subclass_id)
    db_add(_class)
    return _class

def add_spellbook(char_id, spell_id):
    spellbook = Spellbook(char_id, spell_id)
    db_add(spellbook)
    return spellbook


