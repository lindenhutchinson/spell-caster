from app.models.user import User
from app.models.stats import Stats
from app.models.character import Character
from app.models.spellbook import Spellbook
from app.models.spell import Spell
from app.models.slots import Slots
from app.models._class import _Class
from app.utils.model_helpers import *
from app.utils.character_helpers import *
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
import csv


class CharSeeder():

    def __init__(self, app):
        self.app = app

    def run(self):
        
        username = 'a'
        password = 'a'
        if not kw_get_model(User, username=username):
            print("created user:\n\tusername - {}\n\tpassword - {}".format(username, password))
            user = User(username, password)
            insert_model(user)
        else:
            print("using user:\n\tusername - {}\n\tpassword - {}".format(username, password))
            user = kw_get_model(User, username=username)

        name = 'Guh'
        class_id = kw_get_model(_Class, name='Druid').id
        level = 8
        if kw_get_model(Character, name=name):
            kw_delete_model(Character, name=name)
            print("the old guh has been decomposed")
        char = Character(name, level, class_id, user)
        insert_model(char)
        print("created a character named {}".format(name))
        insert_model(Slots(char))
        print("created slots")

        insert_model(Stats(char, 11, 15, 11, 20, 12, 11, 17, 55, 15, 7))
        print("created stats")
        _class = kw_get_model(_Class, name='Druid')

        for sc in _class.spells:
            if sc.spell.level > 0:
                insert_model(Spellbook(char.id, sc.spell))

        spell_names = ['Chill Touch', 'Shape Water',
                       'Shillelagh', 'Thorn Whip',
                       'Blindness/Deafness', 'Gentle Repose (Ritual)',
                       'Animate Dead', 'Gaseous Form',
                       'Blight', 'Confusion']

        known_spells = [sb.spell.id for sb in kw_get_models(Spellbook, char_id=char.id)]
        for name in spell_names:
            spell = kw_get_model(Spell, name=name)
            if spell and not spell.id in known_spells:
                insert_model(Spellbook(char.id, spell, 1))
            else:
                print("didn't add {} to spellbook".format(name))
        print("created custom spellbooks")
        
        decomp = kw_get_model(Spell, name="Decompose")
        if decomp:
            insert_model(Spellbook, char.id, decomp, 1)
        else:
            decompose = Spell('Decompose', 0, 'Necromancy', '1 action', 'Touch', 'V, S', 'Instantaneous', 'You reach out and touch the corpse of a creature. Over the next minute, the corpse begins to rapidly decompose, sprouting fungus and moss as it begins to degrade into compost and mulch. An odd-colored flower or two may also spring from the corpse in this time. Applicable requirements for resurrection are unaffected by this decomposition', 'Matt Mercer')
            insert_model(decompose)
            insert_model(Spellbook(char.id, decompose, 1))
        print("Created Guh!")
