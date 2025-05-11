import unittest
from config import Config
import os

class TestConfig(unittest.TestCase):
    def test_secret_key_default(self):
        self.assertEqual(Config.SECRET_KEY, 'dev_key_12345')

    def test_sqlalchemy_uri(self):
        expected_prefix = 'sqlite:///'
        self.assertTrue(Config.SQLALCHEMY_DATABASE_URI.startswith(expected_prefix))
        self.assertIn('app.db', Config.SQLALCHEMY_DATABASE_URI)

    def test_track_modifications_flag(self):
        self.assertFalse(Config.SQLALCHEMY_TRACK_MODIFICATIONS)

if __name__ == '__main__':
    unittest.main()
