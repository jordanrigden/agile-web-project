import unittest
from flask import Flask
from forms import WorkoutForm
from datetime import date

class TestWorkoutForm(unittest.TestCase):
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

    def test_valid_workout_form(self):
        form = WorkoutForm(
            date=date.today(),
            description='Morning run',
            activity='Moderate',
            duration=45
        )
        self.assertTrue(form.validate())

    def test_missing_fields(self):
        form = WorkoutForm(
            date=None,
            description='',
            activity='',
            duration=None
        )
        self.assertFalse(form.validate())
        self.assertIn('date', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('activity', form.errors)
        self.assertIn('duration', form.errors)

    def test_invalid_duration(self):
        form = WorkoutForm(
            date=date.today(),
            description='Evening walk',
            activity='Light',
            duration=0  # Invalid duration
        )
        self.assertFalse(form.validate())
        self.assertIn('duration', form.errors)

    def test_future_date(self):
        future = date.today().replace(year=date.today().year + 1)
        form = WorkoutForm(
            date=future,
            description='Future run',
            activity='Vigorous',
            duration=30
        )
        self.assertFalse(form.validate())
        self.assertIn('date', form.errors)

if __name__ == "__main__":
    unittest.main()
