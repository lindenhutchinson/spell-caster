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

    # tests
    def test_user_register_form_displays(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_valid_user_register(self):
        self.client.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Created user!', response.data)

    def test_missing_field_user_registration_error(self):
        self.client.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@gmail.com', '')
        self.assertIn(b'Register', response.data)

    def test_login_form_displays(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_login(self):
        self.client.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.client.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Logout', response.data)

    def test_login_without_registering(self):
        self.client.get('/login', follow_redirects=True)
        response = self.login('not-a-real-user', 'FlaskIsAwesome')
        self.assertIn(b'Invalid username or password', response.data)

    def test_valid_logout(self):
        self.client.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.client.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Logout', response.data)

        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)


if __name__ == '__main__':
    unittest.main()
