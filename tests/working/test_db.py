from app.models.user import User
from app.models.character import Character
from app.models.spell import Spell
from app.models.spellclass import SpellClass
from app.models.spellbook import Spellbook
from app.models._class import _Class
from app.models.slots import Slots
from app.models.stats import Stats
from app.models.note import Note
from app.models.action import Action
from app.db.db import db

import unittest

from app.app import create_app, register_extensions
from app.config.config import TestingConfig

from app.utils.model_helpers import insert_model, delete_model, get_model, get_default

# Create an instance of each DB model

class TestFunction(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        db.init_app(self.app)
        register_extensions(self.app)
        self.client = self.app.test_client
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_db(self):
        with self.app.app_context():
            user = User("user name", "password")
            insert_model(user)
            _class = _Class("Druid", "This is the description for a druid")
            insert_model(_class)
            char = Character(
                name = 'Tez',
                level = 5,
                user=user,
                class_id=_class.id
            )
            insert_model(char)

            stats = Stats(
                character=char, 
                str_=10, 
                con_=12, 
                dex_=5, 
                wis_=2, 
                int_=5, 
                chr_=15, 
                ac=24, 
                max_hp=15, 
                spell_save=26, 
                spell_attack=12
            )
            insert_model(stats)

            action = Action(
                character=char, 
                name="The best action ever", 
                desc="This action is just the best bu tyou can only do it once", 
                max_res=1
            )
            insert_model(action)

            spell = Spell(
                name="Sexy guitar time", 
                level=5, 
                school="rock school", 
                cast_time="1 action", 
                spell_range="Touch", 
                components="1 guitar which is destroyed", 
                duration="1 minute", 
                info="sexy guitar time, what else is there to say", 
                from_book="you don't want to know", 
                scaling='this spell doesnt scale pleb', 
                concentration=1
            )
            insert_model(spell)

            spellclass= SpellClass(_class, spell)
            insert_model(spellclass)

            spellbook = Spellbook(char, spell)
            insert_model(spellbook)

            slot = Slots(char)
            insert_model(slot)

            note = Note("this is a title", "this is a body", char.id)
            insert_model(note)

            # test user has a character
            self.assertEqual(user.characters[0], char)
            # test class has a character
            self.assertEqual(_class.characters[0], char)
            # test character has a class
            self.assertEqual(char._class, _class)
            # test character has a slot
            self.assertEqual(char.slots[0], slot)
            # test character has a note
            self.assertEqual(char.notes[0], note)

            # test character has a statistics
            self.assertEqual(char.stats[0], stats)

            # test character has a statistics
            self.assertEqual(char.actions[0], action)

            # test spells have classes
            self.assertEqual(_class.spells, spell.classes)

            # test character has a spellbook which has a spell
            self.assertEqual(char.spellbook[0].spell, spell)

            # test can get a model by ID
            my_char = get_model(Character, char.id)
            self.assertEqual(my_char, char)

            # test can get a default model
            my_spell = get_default(Spell)
            self.assertEqual(my_spell, spell)

            # test can delete a model
            delete_model(note)
            deleted_note = get_model(Note, note.id)
            self.assertEqual(None, deleted_note)

          
    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()