from app.models.user import User
from app.models.character import Character
from app.models.spell import Spell
from app.models.spellbook import Spellbook
from app.models._class import _Class
from app.models.subclass import Subclass
from app.models.slots import Slots

import unittest

from app.app import create_app, register_extensions
from app.db import db
from app.config.config import TestingConfig



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

    def add_character(self, name, race, user_id):
        char = Character(name, race, user_id)
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


    def add_class(self, char_id, name, level, desc, saving_throw, ability_score,subclass_id):
        _class = _Class(char_id, name, level, desc, saving_throw, ability_score, subclass_id)
        self.db_add(_class)
        return _class

    def add_spellbook(self, char_id, spell_id):
        spellbook = Spellbook(char_id, spell_id)
        self.db_add(spellbook)
        return spellbook

    def add_slots(self, char_id):
        slots = Slots(char_id)
        self.db_add(slots)
        return slots

    def test_db(self):
        with self.app.app_context():
            user = self.add_user("user name", "password")
            char = self.add_character("testname", "test race", user.get_id())
            subclass = self.add_subclass("subclass name", "subclass description!", "class resource name")
            _class = self.add_class(char.id, "test class name", 5, "test class description", "wisdom", 8, subclass.id)
            spell = self.add_spell("this is a real spell")
            spellbook = self.add_spellbook(char.id, spell.id)


    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.db.session.remove()
            db.db.drop_all()


if __name__ == '__main__':
    unittest.main()