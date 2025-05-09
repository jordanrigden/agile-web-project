import unittest
from app.forms import RegisterForm
from flask import Flask

class TestRegisterForm(unittest.TestCase):
    def setUp(self):
        # Set up a minimal Flask app context
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_valid_form(self):
        form = RegisterForm(
            username="testuser",
            email="test@example.com",
            weight=65.5,
            password="password123",
            confirm_password="password123"
        )
        self.assertTrue(form.validate())

    def test_missing_fields(self):
        form = RegisterForm(username="", email="", password="", confirm_password="")
        self.assertFalse(form.validate())

    def test_password_mismatch(self):
        form = RegisterForm(
            username="user1",
            email="a@a.com",
            weight=70,
            password="abc",
            confirm_password="xyz"
        )
        self.assertFalse(form.validate())
        self.assertIn('confirm_password', form.errors)

if __name__ == "__main__":
    unittest.main()
