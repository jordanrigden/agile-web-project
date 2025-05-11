import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class TestSeleniumRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        # options.add_argument('--headless')  # Uncomment to hide browser during testing
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')  # Set a larger window size
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get("http://localhost:5000/register")  # Open the register page

    def test_register_success(self):
        driver = self.driver
        
        # Fill out the registration form fields
        driver.find_element(By.NAME, "username").send_keys("selenium_user")
        driver.find_element(By.NAME, "email").send_keys("selenium@example.com")
        driver.find_element(By.NAME, "weight").send_keys("70")
        driver.find_element(By.NAME, "password").send_keys("Selenium123")
        driver.find_element(By.NAME, "confirm_password").send_keys("Selenium123")

        # Locate the submit button
        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "submit"))
        )
        
        # Ensure the button is visible
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(1)  # Wait for scroll to complete

        # Use JavaScript to click the submit button
        driver.execute_script("arguments[0].click();", submit_btn)

        # Wait for the page to load after submission
        time.sleep(2)

        # Assert that we are redirected to the login page with a success message
        self.assertIn("login", driver.current_url.lower())
        self.assertIn("Registration successful", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # Close the browser window
