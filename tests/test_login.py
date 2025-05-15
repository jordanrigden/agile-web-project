import unittest
from flask import Flask
from forms import LoginForm  # Adjust if needed

class TestLoginForm(unittest.TestCase):
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

    def test_valid_login(self):
        form = LoginForm(
            username='testuser',
            password='password123'
        )
        self.assertTrue(form.validate())

    def test_missing_username(self):
        form = LoginForm(
            username='',
            password='password123'
        )
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

    def test_missing_password(self):
        form = LoginForm(
            username='testuser',
            password=''
        )
        self.assertFalse(form.validate())
        self.assertIn('password', form.errors)
# ✅ Print test summary
print("✅ test_login.py ran successfully.")        

if __name__ == "__main__":
    unittest.main()
