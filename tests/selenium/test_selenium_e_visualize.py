import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from server_utils import ServerThread  # ✅ Import the server thread utility

class TestSeleniumVisualize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ✅ Start the Flask live server
        cls.server = ServerThread()
        cls.server.start()
        time.sleep(1)

        # ✅ Set up Chrome WebDriver
        options = Options()
        # options.add_argument('--headless')  # Uncomment for headless testing
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        # ✅ Log in first before running visualization tests
        cls.driver.get("http://127.0.0.1:5000/login")
        cls.driver.find_element(By.NAME, "username").send_keys("selenium01")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        # ✅ Close browser and stop server
        time.sleep(2)
        cls.driver.quit()
        cls.server.shutdown()

    def test_visualize_week(self):
        self.driver.get("http://127.0.0.1:5000/visualize?range=week")
        time.sleep(3)
        self.assertIn("Week Summary", self.driver.page_source)

    def test_visualize_month(self):
        self.driver.get("http://127.0.0.1:5000/visualize?range=month")
        time.sleep(3)
        self.assertIn("Month Summary", self.driver.page_source)

    def test_visualize_year(self):
        self.driver.get("http://127.0.0.1:5000/visualize?range=year")
        time.sleep(3)
        self.assertIn("Year Summary", self.driver.page_source)
        
        # ✅ Print test summary
        print("✅ test_selenium_e_visualize.py ran successfully.")

if __name__ == "__main__":
    unittest.main()
