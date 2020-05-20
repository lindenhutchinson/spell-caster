import unittest

from app.app import create_app, register_extensions
from app.db import db
from app.config.config import TestingConfig


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

    # helpers
    def register(self, username, password):
        return self.client.post(
            '/register',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def create_char(self, name, race, level, saving_throw, ability_score, class_id):
        return self.client.post(
            '/char/create',
            data=dict(name=name, race=race,level=level,saving_throw=saving_throw,ability_score=ability_score, class_id=class_id),
            follow_redirects=True
        )

    # tests
    def test_char_needs_authentication(self):
        response = self.client.get('/char', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login first!', response.data)

    # def test_can_create_character(self):
    #     self.register('patkennedy79@gmail.com', 'FlaskIsAwesome')
    #     self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
    #     self.create_char("Tez","Tortle",7,"Wisdom",4,1)
        # test writing halted until classes have been scrapped!


if __name__ == '__main__':
    unittest.main()
