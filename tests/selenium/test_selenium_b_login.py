import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSeleniumLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Chrome WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)  # Wait for elements to load
        cls.driver.get("http://127.0.0.1:5000/login")  # Ensure Flask app is running

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)  # Allow time to see result
        cls.driver.quit()

    def test_login(self):
        driver = self.driver

        # Fill out login form
        driver.find_element(By.NAME, "username").send_keys("selenium_user")
        driver.find_element(By.NAME, "password").send_keys("Selenium123")
        driver.find_element(By.NAME, "submit").click()

        # Wait for redirect and flash message
        time.sleep(2)

        # Assert login was successful
        self.assertIn("FitTrack", driver.page_source)  # Homepage branding check
        self.assertIn("Logged in successfully.", driver.page_source)  # Flash message check
        self.assertNotIn("/login", driver.current_url)  # Ensure we didn't land back on login

if __name__ == "__main__":
    unittest.main()
