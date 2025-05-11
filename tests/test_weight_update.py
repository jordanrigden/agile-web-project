import unittest
from flask import Flask
from forms import WeightUpdateForm

class TestWeightUpdateForm(unittest.TestCase):
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

    def test_valid_weight(self):
        form = WeightUpdateForm(weight=70.5)
        self.assertTrue(form.validate())

    def test_invalid_weight(self):
        form = WeightUpdateForm(weight=0)
        self.assertFalse(form.validate())
        self.assertIn('weight', form.errors)

        form = WeightUpdateForm(weight=-10)
        self.assertFalse(form.validate())
        self.assertIn('weight', form.errors)

if __name__ == "__main__":
    unittest.main()
