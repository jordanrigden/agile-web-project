import unittest
from flask import Flask
from forms import ShareForm

class TestShareForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        self.request_context.pop()
        self.app_context.pop()

    def test_valid_share(self):
        form = ShareForm(username='validuser', workout_id=1)
        form.workout_id.choices = [(1, 'Workout A')]
        self.assertTrue(form.validate())

    def test_invalid_username_length(self):
        form = ShareForm(username='abc', workout_id=1)
        form.workout_id.choices = [(1, 'Workout A')]
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

        form = ShareForm(username='a' * 26, workout_id=1)
        form.workout_id.choices = [(1, 'Workout A')]
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

# ✅ Print test summary
print("✅ test_share.py ran successfully.")

if __name__ == "__main__":
    unittest.main()
