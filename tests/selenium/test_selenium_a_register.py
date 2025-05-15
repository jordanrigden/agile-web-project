import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from server_utils import ServerThread  # ✅ Import the Flask server thread utility

class TestSeleniumRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ✅ Start the Flask live server
        cls.server = ServerThread()
        cls.server.start()
        time.sleep(1)  # Wait a moment for the server to start

        # ✅ Set up the Chrome browser for testing
        options = Options()
        # options.add_argument('--headless')  # Uncomment to run in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)

        # ✅ Open the registration page
        cls.driver.get("http://127.0.0.1:5000/register")

    def test_register_success(self):
        driver = self.driver

        # ✅ Fill out the registration form fields
        driver.find_element(By.NAME, "username").send_keys("selenium_user")
        driver.find_element(By.NAME, "email").send_keys("selenium@example.com")
        driver.find_element(By.NAME, "weight").send_keys("70")
        driver.find_element(By.NAME, "password").send_keys("Selenium123")
        driver.find_element(By.NAME, "confirm_password").send_keys("Selenium123")

        # ✅ Wait for the submit button to appear
        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "submit"))
        )

        # ✅ Scroll to the submit button and click it via JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)  # Allow scroll animation to complete
        driver.execute_script("arguments[0].click();", submit_btn)

        # ✅ Wait for the next page to load
        time.sleep(2)

        # ✅ Assertions to check if registration was successful
        self.assertIn("login", driver.current_url.lower())
        self.assertIn("Registration successful", driver.page_source)

        # ✅ Print test summary
        print("✅ test_selenium_a_register.py ran successfully.")
    @classmethod
    def tearDownClass(cls):
        # ✅ Quit browser and stop the Flask server
        cls.driver.quit()
        cls.server.shutdown()
