import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSeleniumShare(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.get("http://127.0.0.1:5000/login")

        # Login with valid user
        cls.driver.find_element(By.NAME, "username").send_keys("selenium_user")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_share_workout(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/share")
        time.sleep(1)

        # Share with yourself (to avoid missing user error)
        driver.find_element(By.ID, "shareWithInput").send_keys("selenium_user")

        # Select a workout
        workout_dropdown = driver.find_element(By.NAME, "workout_id")
        options = workout_dropdown.find_elements(By.TAG_NAME, "option")
        if len(options) > 0:
            options[0].click()
        else:
            self.fail("No workouts available to share.")

        # Click the 'Share' button
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # Check if share was successful (adapt to your app's behavior)
        self.assertTrue("/share" not in driver.current_url or "FitTrack" in driver.page_source)

if __name__ == "__main__":
    unittest.main()
