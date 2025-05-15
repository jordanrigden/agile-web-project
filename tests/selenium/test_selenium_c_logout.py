import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from server_utils import ServerThread  # ✅ Import the live Flask server launcher

class TestSeleniumLogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ✅ Start Flask live server
        cls.server = ServerThread()
        cls.server.start()
        time.sleep(1)

        # ✅ Set up Chrome WebDriver
        options = Options()
        # options.add_argument('--headless')  # Uncomment for headless execution
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        # ✅ Navigate to login and log in first
        cls.driver.get("http://127.0.0.1:5000/login")
        cls.driver.find_element(By.NAME, "username").send_keys("selenium01")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(1)

    def test_logout(self):
        driver = self.driver

        # ✅ Visit the logout route
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)

        # ✅ Assert redirect target
        current_url = driver.current_url
        print("Redirected URL after logout:", current_url)
        self.assertTrue(
            current_url == "http://127.0.0.1:5000/" or "login" in current_url.lower()
        )

        # ✅ Assert content shows login prompt or confirmation
        page_source = driver.page_source
        self.assertTrue(
            "Login" in page_source or "logged out" in page_source.lower()
        )

        # ✅ Optionally, check for a login link
        login_links = driver.find_elements(By.LINK_TEXT, "Login")
        self.assertTrue(len(login_links) > 0)

        # ✅ Print test summary
        print("✅ test_selenium_c_logout.py ran successfully.")

    @classmethod
    def tearDownClass(cls):
        # ✅ Quit browser and stop Flask server
        time.sleep(2)
        cls.driver.quit()
        cls.server.shutdown()

if __name__ == "__main__":
    unittest.main()
