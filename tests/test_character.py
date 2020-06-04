import unittest
import flask_testing
from app.models.user import User
from app.models.character import Character
from app.models._class import _Class

from app.app import create_app, register_extensions
# from app.db import db
import flask
from app.config.config import TestingConfig

from app.utils.test_helpers import *

# TODO tests:
# test user is redirected to character page if exists after deleting character
# test user cannot view another user's character
# test user cannot delete another user's character
# test user cannot edit another user's character
# test user can have multiple characters and can cycle by using a session variable
# test deleting a character deletes all notes, slots and spellbooks

class TestFunction(flask_testing.TestCase):

    def create_app(self):
        self.app = create_app(TestingConfig)
        db.db.init_app(self.app)
        register_extensions(self.app)
        self.client = self.app.test_client()
        with self.app.app_context():
            # create all tables
            db.db.create_all()

        return self.app

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.db.session.remove()
            db.db.drop_all()

    def create_and_login_user(self, username, password):
        user = User(username, password)
        insert_model(user)
        self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def create_char(self, name, race, level, casting_ability, ability_score, class_id):
        return self.client.post(
            '/char/create',
            data=dict(name=name, race=race, level=level, casting_ability=casting_ability,
                      ability_score=ability_score, class_id=class_id),
            follow_redirects=True
        )

    def edit_char(self, name, race, level, casting_ability, ability_score, class_id):
        return self.client.post(
            '/char/edit',
            data=dict(name=name, race=race, level=level, casting_ability=casting_ability,
                      ability_score=ability_score, class_id=class_id),
            follow_redirects=True
        )

    def delete_char(self):
        return self.client.get(
            '/char/delete',
            follow_redirects=True
        )


##################################################################################################################
    # tests

    def test_char_needs_authentication(self):
        response = self.client.get('/char', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login first!', response.data)

    def test_can_create_character(self):
        with self.app.app_context():
            # setup test by creating a class
            c_name = b"Druid"
            c_desc = "This is the description for druid"
            _class = _Class(c_name, c_desc)
            insert_model(_class)

            # create a user and log them in
            u_name = "Test User"
            u_pass = "password"
            self.create_and_login_user(u_name, u_pass)

            # define the variables that will be used to create the character
            ch_name = b"Test Char"
            race = b"This is a race"
            level = 5
            mod = 4
            mod_name = "Wisdom"
            class_id = _class.id

            # send a request to create a new character
            response = self.create_char(
                ch_name, race, level, mod_name, mod, class_id)

            # assert we have created a character and have been redirected to its page
            self.assertIn(c_name, response.data)
            self.assertIn(ch_name, response.data)
            self.assertIn(race, response.data)

    def test_user_can_edit_character(self):
        with self.app.app_context():
            # setup test by creating a class
            c_name = b"Druid"
            c_desc = "This is the description for druid"
            _class = _Class(c_name, c_desc)
            insert_model(_class)

            # create a user and log them in
            u_name = "Test User"
            u_pass = "password"
            self.create_and_login_user(u_name, u_pass)

            # define the variables that will be used to create the character
            ch_name = b"Test Char"
            race = b"This is a race"
            level = 5
            mod = 4
            mod_name = "Wisdom"
            class_id = _class.id

            # send a request to create a new character
            response = self.create_char(
                ch_name, race, level, mod_name, mod, class_id)
                
            # assert we have created a character and have been redirected to its page
            self.assertIn(c_name, response.data)
            self.assertIn(ch_name, response.data)
            self.assertIn(race, response.data)

            # create a new class
            c_name = b"Wizard"
            c_desc = "This is the description for wizard"
            _class = _Class(c_name, c_desc)
            insert_model(_class)

            # define new variables to update the current character with
            ch_name_2 = b"New character"
            race = b"This is a new race"
            level = 10
            mod = 8
            mod_name = "Strength"
            class_id = _class.id

            # send a request to update the character
            response = self.edit_char(
                ch_name_2, race, level, mod_name, mod, class_id)

            # assert the values have been updated on the character page
            self.assertIn(c_name, response.data)
            self.assertIn(ch_name_2, response.data)
            self.assertIn(race, response.data)

    def test_can_delete_char(self):
        with self.app.app_context():

            # setup test by creating a class
            c_name = b"Druid"
            c_desc = "This is the description for druid"
            _class = _Class(c_name, c_desc)
            insert_model(_class)

            # create a user and log them in
            u_name = "Test User"
            u_pass = "password"
            self.create_and_login_user(u_name, u_pass)

            # define the variables that will be used to create the character
            ch_name = b"Test Char"
            race = b"This is a race"
            level = 5
            mod = 4
            mod_name = "Wisdom"
            class_id = _class.id

            # send a request to create a new character
            response = self.create_char(
                ch_name, race, level, mod_name, mod, class_id)
                
            # assert we have created a character and have been redirected to its page
            self.assertIn(c_name, response.data)
            self.assertIn(ch_name, response.data)
            self.assertIn(race, response.data)

            # send a request to delete the current character
            response = self.delete_char()

            # as the current user has no more characters, assert we have been redirected to the homepage
            self.assertIn(b"homepage", response.data)

if __name__ == '__main__':
    unittest.main()
