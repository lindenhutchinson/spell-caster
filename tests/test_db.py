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

    def add_character(self, name, race, level, saving_throw, ability_score,user, class_id):
        char = Character(name, level, race, saving_throw, ability_score, user, class_id)
        self.db_add(char)
        return char

    def add_spell(self, name, level, cast_time, concentration, ritual,spell_range, components, duration, school, info, from_book, is_bard, is_cleric, is_druid, is_paladin, is_ranger, is_sorcerer, is_warlock, is_wizard):
        spell = Spell(name, level, cast_time, concentration, ritual, spell_range, components, duration, school, info, from_book, is_bard, is_cleric, is_druid, is_paladin, is_ranger, is_sorcerer, is_warlock, is_wizard)
        self.db_add(spell)
        return spell


    def add_class(self, name, desc):
        _class = _Class(name, desc)
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

    def add_note(self, title, body, character):
        note = Note(title, body, character)
        self.db_add(note)
        return note

    def test_db(self):
        with self.app.app_context():
            user = self.add_user("user name", "password")
            _class = self.add_class("Druid", "This is the description for a druid")
            char = self.add_character("Tez", 7, "Tortle", "wisdom", 4, user, _class.id)
            spell = self.add_spell("spell_name",5,"Instant",1,1,"5 feet","All of them","it takes forever","school of rock", "this is some very important info","the bible", 1, 1, 0, 1, 1, 1, 1, 1)
            spellbook = self.add_spellbook(char, spell)
            slot = self.add_slots(char, 1, 4)
            note = self.add_note("this is a title", "this is a body", char.id)

            self.assertEqual(user.characters[0], char)
            self.assertEqual(_class.characters[0], char)
            self.assertEqual(char._class, _class)
            self.assertEqual(char.slots[0], slot)
            self.assertEqual(char.notes[0], note)
            self.assertEqual(spellbook.spell, spell)
            self.assertEqual(spellbook.character, char)
            self.assertEqual(char.spellbook[0].spell, spell)



          


    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.db.session.remove()
            db.db.drop_all()


if __name__ == '__main__':
    unittest.main()