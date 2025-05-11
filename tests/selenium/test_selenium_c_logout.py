import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class TestSeleniumLogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Optional: Headless mode settings
        options = Options()
        # options.add_argument('--headless')  # Uncomment to run without a visible browser
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.driver.get("http://127.0.0.1:5000/login")

        # Log in before testing logout
        cls.driver.find_element(By.NAME, "username").send_keys("selenium_user")
        cls.driver.find_element(By.NAME, "password").send_keys("Selenium123")
        cls.driver.find_element(By.NAME, "submit").click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

    def test_logout(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)

        # Assert redirected URL
        current_url = driver.current_url
        print("Redirected URL after logout:", current_url)
        self.assertTrue(
            current_url == "http://127.0.0.1:5000/" or "login" in current_url.lower()
        )

        # Assert page contains "Login" or logout confirmation
        page_source = driver.page_source
        self.assertTrue(
            "Login" in page_source or "logged out" in page_source.lower()
        )

        # Optionally, check for presence of a "Login" link
        login_links = driver.find_elements(By.LINK_TEXT, "Login")
        self.assertTrue(len(login_links) > 0)

if __name__ == "__main__":
    unittest.main()
