import unittest
from flask import Flask
from forms import RegisterForm
from config import Config
 
class TestRegisterForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.ctx = self.app.app_context()
        self.ctx.push()
 
    def tearDown(self):
        self.ctx.pop()
 
    def test_valid_form(self):
        form = RegisterForm(
            username="testuser",
            email="test@example.com",
            weight=70,
            password="password123",
            confirm_password="password123"
        )
        self.assertTrue(form.validate())
 
    def test_password_mismatch(self):
        form = RegisterForm(
            username="testuser",
            email="test@example.com",
            weight=70,
            password="password123",
            confirm_password="wrongpass"
        )
        self.assertFalse(form.validate())
        self.assertIn("Passwords must match", str(form.confirm_password.errors))
 
    def test_invalid_email(self):
        form = RegisterForm(
            username="testuser",
            email="invalid-email",
            weight=70,
            password="password123",
            confirm_password="password123"
        )
        self.assertFalse(form.validate())
 
if __name__ == "__main__":
    unittest.main()