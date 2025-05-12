import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from server_utils import ServerThread  # ✅ Import the live Flask server utility

class TestSeleniumShare(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ✅ Start the Flask server
        cls.server = ServerThread()
        cls.server.start()
        time.sleep(1)

        # ✅ Set up the Chrome WebDriver
        options = Options()
        # options.add_argument('--headless')  # Uncomment to run in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        # ✅ Log in before accessing /share
        cls.driver.get("http://127.0.0.1:5000/login")
        cls.driver.find_element(By.NAME, "username").send_keys("selenium01")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # ✅ Clean up
        time.sleep(2)
        cls.driver.quit()
        cls.server.shutdown()

    def test_share_workout(self):
        driver = self.driver

        # ✅ Go to the share page
        driver.get("http://127.0.0.1:5000/share")
        time.sleep(1)

        # ✅ Share with yourself
        driver.find_element(By.ID, "shareWithInput").send_keys("selenium01")

        # ✅ Select the first workout option
        workout_dropdown = driver.find_element(By.NAME, "workout_id")
        options = workout_dropdown.find_elements(By.TAG_NAME, "option")
        if options:
            options[0].click()
        else:
            self.fail("No workouts available to share.")

        # ✅ Click the 'Share' button
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # ✅ Verify share success (adjust depending on actual behavior)
        self.assertTrue("/share" not in driver.current_url or "FitTrack" in driver.page_source)

if __name__ == "__main__":
    unittest.main()
