# TODO:
# write this test!

# test_can_add_note
# test_can_edit_note
# test_can_delete_note
# test_note_requires_char
# test_note_requires_authentication
# test_char_cant_view_others_notes
# test_char_cant_edit_others_notes
# test_char_cant_delete_others_notes
# test_char_can_have_multiple_notes


import unittest
from app.models.user import User
from app.models.character import Character
from app.models.note import Note
from app.models._class import _Class

from app.app import create_app, register_extensions

from app.config.config import TestingConfig

from app.utils.test_helpers import *

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

    def create_note(self, title, body):
        return self.client.post(
            '/notes/create',
            follow_redirects=True,
            data=dict(title=title, body=body),
        )

    def edit_note(self,id,title,body):
        return self.client.post(
            '/notes/edit?id={}'.format(id),
            data=dict(name=title, desc=body),
            follow_redirects=True
        )

    def view_note(self, id):
        return self.client.get(
            '/notes?id={}'.format(id)
        )

    def delete_note(self, id):
        return self.client.get(
            '/notes/delete?id={}'.format(id),
            follow_redirects=True
        )


    def create_char(self, name, race, level, casting_ability, ability_score, class_id):
        return self.client.post(
            '/char/create',
            data=dict(name=name, race=race, level=level, casting_ability=casting_ability,
                      ability_score=ability_score, class_id=class_id),
            follow_redirects=True
        )


    def create_user_and_character(self):
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

            # send a request to create a new character, which will set the newly created char as active
            self.create_char(
                ch_name, race, level, mod_name, mod, class_id)
                
    

######################################################
#tests

    def test_create_note_needs_authentication(self):
        response = self.client.get('/notes/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login first!', response.data)

    def test_create_note_needs_character(self):
        self.create_and_login_user('username','password')
        response = self.client.get('/notes/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please create a character', response.data)

    def test_can_create_note(self):
        self.create_user_and_character()
        title=b"this is a note title"
        body=b"this is the body of the note"
        response = self.create_note(title, body)
        self.assertIn(title, response.data)
        self.assertIn(body, response.data)


    # Need to be able to keep track of a note ID so it is possible to edit
    # and delete a specific note!
    
    # def test_can_edit_note(self):
    #     self.create_user_and_character()
    #     title=b"this is a note title"
    #     body=b"this is the body of the note"
    #     self.create_note(title,body)
    #     new_title=b"this is brand new!"
    #     new_body=b"this is brand new body!!!!!"
    #     self.edit_note()

            