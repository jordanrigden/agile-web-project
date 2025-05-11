import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSeleniumLogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.get("http://127.0.0.1:5000/login")

        # Log in first
        cls.driver.find_element(By.NAME, "username").send_keys("selenium_user")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_logout(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)

        # Print actual redirected URL for debugging
        current_url = driver.current_url
        print("Redirected URL after logout:", current_url)

        # More reliable check: most systems redirect to login page
        self.assertIn("login", current_url.lower())  

        # Check if login prompt or flash message is present
        page_source = driver.page_source
        self.assertTrue("Login" in page_source or "Logged out successfully" in page_source)

if __name__ == "__main__":
    unittest.main()
