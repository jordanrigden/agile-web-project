import unittest
from app import app
from config import Config

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        app.config.from_object(Config)
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html', response.data)  # generic HTML check

    def test_register_route(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        
# ✅ Print test summary
print("✅ test_app.py ran successfully.")

if __name__ == '__main__':
    unittest.main()
