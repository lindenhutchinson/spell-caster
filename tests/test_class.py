import unittest
from app.models.user import User
from app.models.character import Character
from app.models._class import _Class

from app.app import create_app, register_extensions
# from app.db import db

from app.config.config import TestingConfig

from app.utils.test_helpers import *

# TODO:
# test class cannot be deleted if being used by characters


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

    def create_class(self, name, desc):
        return self.client.post(
            '/class/create',
            data=dict(name=name, desc=desc),
            follow_redirects=True
        )
    
    def edit_class(self, id, name, desc):
        return self.client.post(
            '/class/edit?id={}'.format(id),
            data=dict(name=name, desc=desc),
            follow_redirects=True
        )

    def delete_class(self, id):
        return self.client.get(
            '/class/delete?id={}'.format(id),
            follow_redirects=True
        )

######################################################
#tests

    def test_class_needs_authentication(self):
        response = self.client.get('/class', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login first!', response.data)

    def test_can_create_class(self):
        self.create_and_login_user("user","password")
        name = b"Druid"
        desc = b"Druid description right here!" 
        response = self.create_class(name, desc)
        self.assertIn(name, response.data)
        self.assertIn(desc, response.data)

    def test_can_edit_class(self):
        with self.app.app_context():
            self.create_and_login_user("user","password")
            name = b"Druid"
            desc = b"Druid description right here!" 
            _class = _Class(name, desc)
            insert_model(_class)
            new_name = b"Wizard"
            new_desc = b"Wizard desc"
            response = self.edit_class(_class.id, new_name, new_desc)
            self.assertIn(new_name, response.data)
            self.assertIn(new_desc, response.data)

    def test_can_delete_class(self):
        with self.app.app_context():
            self.create_and_login_user("user","password")

            name = b"Druid"
            desc = b"Druid description right here!" 
            _class = _Class(name, desc)
            insert_model(_class)

            response = self.delete_class(_class.id)
            self.assertIn(b"homepage", response.data)


