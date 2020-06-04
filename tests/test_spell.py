import unittest
from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.models.spell import Spell

from app.app import create_app, register_extensions

from app.config.config import TestingConfig

from app.utils.test_helpers import *

# TODO:
# write this test!

# test_can_add_spell
# test_can_edit_spell
# test_can_delete_spell
# test_spell_requires_authentication
# test_deleting_spell_deletes_spellbook
# test_updating_spell_updates_spellbook

class TestFunction(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        db.db.init_app(self.app)
        register_extensions(self.app)
        self.client = self.app.test_client()
        with self.app.app_context():
            # create all tables
            db.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.db.session.remove()
            db.db.drop_all()

    def create_and_login_user(self, username, password):
        self.client.post(
            '/register',
            data=dict(username=username, password=password),
            follow_redirects=True
        )
        self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def create_spell(self, name, level, school, cast_time, spell_range, components, duration, text, from_book, scaling=' ', concentration=0,is_bard=0, is_cleric=0, is_druid=0, is_paladin=0, is_ranger=0, is_sorcerer=0, is_warlock=0, is_wizard=0):
        return self.client.post(
            '/spell/create',
            data=dict(name=name, 
            level=level, 
            school=school,
            cast_time=cast_time,
            spell_range=spell_range,
            components=components,
            duration=duration,
            info=text,
            from_book=from_book,
            scaling=scaling,
            concentration=concentration
            ),
            follow_redirects=True
        )

    def edit_spell(self, id, name, level, school, cast_time, spell_range, components, duration, text, from_book, scaling=' ', concentration=0,is_bard=0, is_cleric=0, is_druid=0, is_paladin=0, is_ranger=0, is_sorcerer=0, is_warlock=0, is_wizard=0):
        return self.client.post(
            '/spell/edit?id={}'.format(id),
            data=dict(name=name, 
            level=level, 
            school=school,
            cast_time=cast_time,
            spell_range=spell_range,
            components=components,
            duration=duration,
            info=text,
            from_book=from_book,
            scaling=scaling,
            concentration=concentration
            ),
            follow_redirects=True
        )

    def view_spell(self, id):
        return self.client.get(
            '/spell?id={}'.format(id)
        )

    def delete_spell(self, id):
        return self.client.get(
            '/spell/delete?id={}'.format(id),
            follow_redirects=True
        )

######################################################
#tests

    def test_create_spell_needs_authentication(self):
        response = self.client.get('/spell/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login first!', response.data)

    def test_can_create_spell(self):
        self.create_and_login_user("user","password")
        name=b'spell nam' 
        level=10 
        school=b'spell schoo'
        cast_time=b'cast time'
        spell_range=b'spell range'
        components=b'components'
        duration=b'duration'
        info=b'description of the spell'
        from_book=b'found in this book'
        scaling=b'at higher levels'
        concentration=1
        response = self.create_spell(name, level, school, cast_time, spell_range, components, duration, info, from_book, scaling, concentration)
        self.assertIn(name, response.data)
        self.assertIn(info, response.data)

    def test_can_edit_spell(self):
        with self.app.app_context():
            self.create_and_login_user("user","password")
            name=b'spell nam' 
            level=10 
            school=b'spell schoo'
            cast_time=b'cast time'
            spell_range=b'spell range'
            components=b'components'
            duration=b'duration'
            info=b'description of the spell'
            from_book=b'found in this book'
            scaling=b'at higher levels'
            concentration=1

            spell = Spell(name, level, school, cast_time, spell_range, components, duration, info, from_book, scaling, concentration)
            insert_model(spell)
            
            new_name=b'New spell name!'
            new_info=b'New info!!!!'
            response = self.edit_spell(spell.id, new_name, level, school, cast_time, spell_range, components, duration, new_info, from_book, scaling, concentration)
            self.assertIn(new_name, response.data)
            self.assertIn(new_info, response.data)

    def test_can_delete_spell(self):
        with self.app.app_context():
            self.create_and_login_user("user","password")
            name=b'spell nam' 
            level=10 
            school=b'spell schoo'
            cast_time=b'cast time'
            spell_range=b'spell range'
            components=b'components'
            duration=b'duration'
            info=b'description of the spell'
            from_book=b'found in this book'
            scaling=b'at higher levels'
            concentration=1

            spell = Spell(name, level, school, cast_time, spell_range, components, duration, info, from_book, scaling, concentration)
            insert_model(spell)
            response = self.view_spell(spell.id)
            self.assertIn(name, response.data)
            self.assertIn(info, response.data)
            response = self.delete_spell(spell.id)
            self.assertIn(b"Spell deleted!", response.data)
   