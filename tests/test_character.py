import unittest
import flask_testing
from app.models.user import User
from app.models.character import Character
from app.models._class import _Class

from app.app import create_app, register_extensions
from app.db import db
import flask
from app.config.config import TestingConfig


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

    # helpers
    def db_add(self, o):
        db.db.session.add(o)
        db.db.session.commit()

    def add_user(self, name, password):
        user = User(name, password)
        self.db_add(user)
        return user

    def add_class(self, name, desc):
        _class = _Class(name, desc)
        self.db_add(_class)
        return _class

    def add_character(self, name, race, level, saving_throw, ability_score, user, class_id):
        char = Character(name, race, level, saving_throw,
                         ability_score, user, class_id)
        self.db_add(char)
        return char

    def create_and_login_user(self, username, password):
        user = self.add_user(username, password)
        self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def create_char(self, name, race, level, saving_throw, ability_score, class_id):
        return self.client.post(
            '/char/create',
            data=dict(name=name, race=race, level=level, saving_throw=saving_throw,
                      ability_score=ability_score, class_id=class_id),
            follow_redirects=True
        )

    def edit_char(self, name, race, level, saving_throw, ability_score, class_id):
        return self.client.post(
            '/char/edit',
            data=dict(name=name, race=race, level=level, saving_throw=saving_throw,
                      ability_score=ability_score, class_id=class_id),
            follow_redirects=True
        )

    # currently cannot test deleting a character as session variables need to be accessed during the test
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
            c_name = b"Druid"
            c_desc = "This is the description for druid"

            _class = self.add_class(c_name, c_desc)
            u_name = "Test User"
            u_pass = "password"

            ch_name_1 = b"Test Char"
            race = b"This is a race"
            level = 5
            mod = 4
            mod_name = "Wisdom"
            class_id = _class.id

            self.create_and_login_user(u_name, u_pass)

            response = self.create_char(
                ch_name_1, race, level, mod_name, mod, class_id)

            self.assertIn(c_name, response.data)
            self.assertIn(ch_name_1, response.data)
            self.assertIn(race, response.data)

    def test_user_can_edit_character(self):
        with self.app.app_context():
            c_name = b"Druid"
            c_desc = "This is the description for druid"

            _class = self.add_class(c_name, c_desc)
            u_name = "Test User"
            u_pass = "password"

            ch_name_1 = b"Test Char"
            race = b"This is a race"
            level = 5
            mod = 4
            mod_name = "Wisdom"
            class_id = _class.id

            self.create_and_login_user(u_name, u_pass)

            response = self.create_char(
                ch_name_1, race, level, mod_name, mod, class_id)
            self.assertIn(c_name, response.data)
            self.assertIn(ch_name_1, response.data)
            self.assertIn(race, response.data)
            c_name = b"Wizard"
            c_desc = "This is the description for wizard"
            _class = self.add_class(c_name, c_desc)
            ch_name_2 = b"New character"
            race = b"This is a new race"
            level = 10
            mod = 8
            mod_name = "Strength"
            class_id = _class.id
            response = self.edit_char(
                ch_name_2, race, level, mod_name, mod, class_id)
            self.assertIn(c_name, response.data)
            self.assertIn(ch_name_2, response.data)
            self.assertIn(race, response.data)

    def test_can_delete_char(self):
        with self.app.app_context():

            c_name = b"Druid"
            c_desc = "This is the description for druid"

            _class = self.add_class(c_name, c_desc)
            u_name = "Test User"
            u_pass = "password"

            ch_name_1 = b"Test Char"
            race = b"This is a race"
            level = 5
            mod = 4
            mod_name = "Wisdom"
            class_id = _class.id

            user = self.create_and_login_user(u_name, u_pass)

            self.create_char(
                ch_name_1, race, level, mod_name, mod, class_id)


            response = self.delete_char()
                
            self.assertIn(b"homepage", response.data)


if __name__ == '__main__':
    unittest.main()
