import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from server_utils import ServerThread  # ✅ Import live Flask server thread

class TestSeleniumLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ✅ Start the Flask live server
        cls.server = ServerThread()
        cls.server.start()
        time.sleep(1)  # Wait for the server to boot up

        # ✅ Start Chrome WebDriver with options
        options = Options()
        # options.add_argument('--headless')  # Optional: headless mode for CI
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        # ✅ Navigate to the login page
        cls.driver.get("http://127.0.0.1:5000/login")

    def test_login(self):
        driver = self.driver

        # ✅ Fill out login form
        driver.find_element(By.NAME, "username").send_keys("selenium01")
        driver.find_element(By.NAME, "password").send_keys("Selenium123")
        driver.find_element(By.NAME, "submit").click()

        # ✅ Wait for redirect and success message
        time.sleep(2)

        # ✅ Assertions to verify login worked
        self.assertIn("FitTrack", driver.page_source)  # Check homepage branding
        self.assertIn("Logged in successfully.", driver.page_source)  # Flash message
        self.assertNotIn("/login", driver.current_url)  # Ensure not still on login page

        # ✅ Print test summary
        print("✅ test_selenium_b_login.py ran successfully.")
    @classmethod
    def tearDownClass(cls):
        # ✅ Close browser and stop Flask server
        time.sleep(2)  # Optional: see the result before closing
        cls.driver.quit()
        cls.server.shutdown()

if __name__ == "__main__":
    unittest.main()
