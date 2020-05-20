from app.models.user import User
from app.models.character import Character
from app.models.spell import Spell
from app.models.spellbook import Spellbook
from app.models._class import _Class
from app.models.subclass import Subclass
from app.models.slots import Slots
from app.models.notes import Notes

import unittest

from app.app import create_app, register_extensions
from app.db import db
from app.config.config import TestingConfig


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

    def db_add(self, o):
        db.db.session.add(o)
        db.db.session.commit()

    def add_user(self, name, password):
        user = User(name, password)
        self.db_add(user)
        return user

    def add_character(self, name, race, user):
        char = Character(name, race, user)
        self.db_add(char)
        return char

    def add_spell(self, name):
        spell = Spell(name)
        self.db_add(spell)
        return spell

    def add_subclass(self, name, desc, resource_name):
        subclass = Subclass(name, desc, resource_name)
        self.db_add(subclass)
        return subclass


    def add_class(self, name, level, desc, saving_throw, ability_score, character, subclass):
        _class = _Class(name, level, desc, saving_throw, ability_score, character, subclass)
        self.db_add(_class)
        return _class

    def add_spellbook(self, character, spell):
        spellbook = Spellbook(character, spell)
        self.db_add(spellbook)
        return spellbook

    def add_slots(self, character, lvl, max_val):
        slots = Slots(lvl, max_val, character)
        self.db_add(slots)
        return slots

    def add_notes(self, title, body, character):
        notes = Notes(title, body, character)
        self.db_add(notes)
        return notes

    def test_db(self):
        with self.app.app_context():
            user = self.add_user("user name", "password")
            char = self.add_character("testname", "test race", user)
            subclass = self.add_subclass("subclass name", "subclass description!", "class resource name")
            _class = self.add_class("test class name", 5, "test class description", "wisdom", 8, char, subclass)
            spell = self.add_spell("this is a real spell")
            spellbook = self.add_spellbook(char, spell)
            slot = self.add_slots(char, 1, 4)
            notes = self.add_notes("this is a title", "this is a body", char)

            self.assertEqual(user.characters.one(), char)
            self.assertEqual(char._class, _class)
            self.assertEqual(char.slots, slot)
            self.assertEqual(char.notes, notes)
            self.assertEqual(subclass._class, _class)
            self.assertEqual(spellbook.spell, spell)
            self.assertEqual(spellbook.character, char)


          


    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.db.session.remove()
            db.db.drop_all()


if __name__ == '__main__':
    unittest.main()