import unittest
from flask import Flask
from forms import RegisterForm  # Adjust import if needed
 
class TestRegisterForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
 
        self.app_context = self.app.app_context()
        self.app_context.push()
 
        self.request_context = self.app.test_request_context()
        self.request_context.push()
 
    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()
 
    def test_valid_form(self):
        form = RegisterForm(
            username='testuser',
            email='test@example.com',
            weight=70.0,
            password='password123',
            confirm_password='password123'
        )
        self.assertTrue(form.validate())
 
    def test_missing_fields(self):
        form = RegisterForm(
            username='',
            email='',
            weight=None,
            password='',
            confirm_password=''
        )
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('weight', form.errors)
        self.assertIn('password', form.errors)
 
    def test_password_mismatch(self):
        form = RegisterForm(
            username='user1',
            email='a@a.com',
            weight=60,
            password='abc123',
            confirm_password='xyz123'
        )
        self.assertFalse(form.validate())
        self.assertIn('confirm_password', form.errors)
 
    def test_invalid_email(self):
        form = RegisterForm(
            username='user2',
            email='not-an-email',
            weight=75,
            password='abc12345',
            confirm_password='abc12345'
        )
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
 
    def test_invalid_weight(self):
        form = RegisterForm(
            username='user3',
            email='user@example.com',
            weight=0,  # invalid weight
            password='abc12345',
            confirm_password='abc12345'
        )
        self.assertFalse(form.validate())
        self.assertIn('weight', form.errors)

# ✅ Print test summary
print("✅ test_registration.py ran successfully.")

if __name__ == "__main__":
    unittest.main()