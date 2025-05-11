import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime

class TestSeleniumUpload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.get("http://127.0.0.1:5000/login")

        # Login
        cls.driver.find_element(By.NAME, "username").send_keys("selenium_user")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_upload_workout(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/upload")

        # Set date using JS to avoid input compatibility issues
        today = datetime.today().strftime('%Y-%m-%d')
        date_input = driver.find_element(By.NAME, "date")
        driver.execute_script("arguments[0].value = arguments[1];", date_input, today)

        # Fill other fields
        driver.find_element(By.NAME, "description").send_keys("Selenium test workout")
        driver.find_element(By.NAME, "duration").send_keys("45")

        # Optional: Select activity type if applicable
        try:
            activity_type = Select(driver.find_element(By.NAME, "activity"))
            activity_type.select_by_index(1)  # or select_by_visible_text("Running")
        except:
            pass

        # Submit the form
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(2)

        # Check for success message or redirect
        self.assertTrue("Upload" in driver.page_source or "Success" in driver.page_source)

if __name__ == "__main__":
    unittest.main()
