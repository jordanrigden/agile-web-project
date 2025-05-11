import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSeleniumVisualize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.get("http://127.0.0.1:5000/login")

        # Log in first (reuse login logic)
        cls.driver.find_element(By.NAME, "username").send_keys("mehnaz")
        cls.driver.find_element(By.NAME, "password").send_keys("123456")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_visualize_week(self):
        self.driver.get("http://127.0.0.1:5000/visualize?range=week")
        time.sleep(1)
        self.assertIn("Week Summary", self.driver.page_source)

    def test_visualize_month(self):
        self.driver.get("http://127.0.0.1:5000/visualize?range=month")
        time.sleep(1)
        self.assertIn("Month Summary", self.driver.page_source)

    def test_visualize_year(self):
        self.driver.get("http://127.0.0.1:5000/visualize?range=year")
        time.sleep(1)
        self.assertIn("Year Summary", self.driver.page_source)

if __name__ == "__main__":
    unittest.main()
