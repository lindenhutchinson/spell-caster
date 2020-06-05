from app.models.user import User
from app.models.character import Character
from app.models.spell import Spell
from app.models.spellbook import Spellbook
from app.models._class import _Class
from app.models.subclass import Subclass
from app.models.slots import Slots
from app.models.note import Note

import unittest

from app.app import create_app, register_extensions
from app.config.config import TestingConfig

from app.utils.test_helpers import *

# Create an instance of each DB model

class TestFunction(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        db.db.init_app(self.app)
        register_extensions(self.app)
        self.client = self.app.test_client
        with self.app.app_context():
            # create all tables
            db.db.create_all()

    def test_db(self):
        with self.app.app_context():
            user = User("user name", "password")
            insert_model(user)
            _class = _Class("Druid", "This is the description for a druid")
            insert_model(_class)
            char = Character("Tez", "Tortle", 7,"wisdom", 4, _class.id, user)
            insert_model(char)
            spell = Spell("spell_name",5,"Instant","5 feet","All of them","it takes forever","school of rock", "this is some very important info","the bible",1,1, 1, 1, 0, 1, 1, 1, 1, 1)
            insert_model(spell)
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
            # test spellbook has a spell
            self.assertEqual(spellbook.spell, spell)
            # test spellbook has a character
            self.assertEqual(spellbook.character, char)
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
            db.db.session.remove()
            db.db.drop_all()


if __name__ == '__main__':
    unittest.main()