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
        cls.driver.find_element(By.NAME, "username").send_keys("mehnaz")
        cls.driver.find_element(By.NAME, "password").send_keys("123456")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_logout(self):
        self.driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)

        # Check if redirected to homepage
        current_url = self.driver.current_url
        self.assertTrue(current_url.endswith("/") or "home" in current_url)

        # Check for login prompt or logout message on homepage
        page_source = self.driver.page_source
        self.assertTrue("Login" in page_source or "Logged out successfully" in page_source)

if __name__ == "__main__":
    unittest.main()
