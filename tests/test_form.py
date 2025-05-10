import unittest
from flask import Flask
from flask_wtf import CSRFProtect
from forms import RegisterForm
from config import Config

class TestFormConfig(Config):
    WTF_CSRF_ENABLED = False  # Disable CSRF for form testing

class FormValidationTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(TestFormConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_valid_form(self):
        form = RegisterForm(data={
            'username': 'ValidUser',
            'email': 'user@example.com',
            'password': 'SecurePass123',
            'confirm_password': 'SecurePass123'
        })
        self.assertTrue(form.validate())

    def test_invalid_email(self):
        form = RegisterForm(data={
            'username': 'User',
            'email': 'invalid-email',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        form = RegisterForm(data={
            'username': 'User',
            'email': 'user@example.com',
            'password': 'pass123',
            'confirm_password': 'differentpass'
        })
        self.assertFalse(form.validate())
        self.assertIn('confirm_password', form.errors)

    def test_empty_fields(self):
        form = RegisterForm(data={})
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)

    def test_username_length_constraint(self):
        form = RegisterForm(data={
            'username': 'abc',  # too short
            'email': 'user@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

if __name__ == '__main__':
    unittest.main()
