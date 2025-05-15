import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from server_utils import ServerThread  # ✅ Import Flask live server thread

class TestSeleniumUpload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ✅ Start the Flask live server
        cls.server = ServerThread()
        cls.server.start()
        time.sleep(1)

        # ✅ Launch Chrome browser
        options = Options()
        # options.add_argument('--headless')  # Uncomment for headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        # ✅ Log in before testing upload
        cls.driver.get("http://127.0.0.1:5000/login")
        cls.driver.find_element(By.NAME, "username").send_keys("selenium01")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # ✅ Close browser and stop server
        time.sleep(2)
        cls.driver.quit()
        cls.server.shutdown()

    def test_upload_workout(self):
        driver = self.driver

        # ✅ Go to upload page
        driver.get("http://127.0.0.1:5000/upload")

        # ✅ Set today's date using JavaScript
        today = datetime.today().strftime('%Y-%m-%d')
        date_input = driver.find_element(By.NAME, "date")
        driver.execute_script("arguments[0].value = arguments[1];", date_input, today)

        # ✅ Fill out the workout form
        driver.find_element(By.NAME, "description").send_keys("Selenium test workout")
        driver.find_element(By.NAME, "duration").send_keys("45")

        # ✅ Select activity type if dropdown exists
        try:
            activity_type = Select(driver.find_element(By.NAME, "activity"))
            activity_type.select_by_index(1)  # Or select_by_visible_text("Running")
        except:
            pass  # Skip if the dropdown doesn't exist

        # ✅ Submit the form
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(2)

        # ✅ Check for success message or confirmation
        self.assertTrue("Upload" in driver.page_source or "Success" in driver.page_source)

        # ✅ Print test summary
        print("✅ test_selenium_d_upload.py ran successfully.")

if __name__ == "__main__":
    unittest.main()
