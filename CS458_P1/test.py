import unittest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class LoginPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the local web server on port 3000 in the background
        cls.server_process = subprocess.Popen(["python3", "-m", "http.server", "3000"])
        time.sleep(2)  # Wait for the server to start

        options = webdriver.ChromeOptions()
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")  # Only for local testing!
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

        cls.base_url = "http://localhost:3000/index.html"

    @classmethod
    def tearDownClass(cls):
        cls.driver.implicitly_wait(100)
        cls.server_process.terminate()
        cls.driver.quit()

    def setUp(self):
        print(f"\n[INFO] Navigating to {self.base_url}")
        self.driver.get(self.base_url)
        time.sleep(2)  # Allow time for the page to load

    def test_valid_standard_login(self):
        """Test Case #1: Valid Standard Login"""
        driver = self.driver
        try:
            print("[DEBUG] Attempting standard login...")

            email_field = driver.find_element(By.ID, "emailInput")
            password_field = driver.find_element(By.ID, "passwordInput")
            login_button = driver.find_element(By.CLASS_NAME, "btn-login")

            print(f"[DEBUG] Email field displayed: {email_field.is_displayed()}")
            print(f"[DEBUG] Password field displayed: {password_field.is_displayed()}")
            print(f"[DEBUG] Login button displayed: {login_button.is_displayed()}")

            email_field.send_keys("john@example.com")
            password_field.send_keys("12345")
            login_button.click()
            print("[DEBUG] Clicked login button")

            success_msg = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "message"))
            )
            print(f"[DEBUG] Success message received: {success_msg.text}")

            self.assertIn("Login Successful", success_msg.text)

        except Exception as e:
            print("[ERROR] Standard login test failed")
            self.fail(str(e))

    def test_invalid_password(self):
        """Test Case #2: Invalid Password"""
        driver = self.driver
        try:
            print("[DEBUG] Testing invalid password...")

            driver.find_element(By.ID, "emailInput").send_keys("john@example.com")
            driver.find_element(By.ID, "passwordInput").send_keys("wrongpass")
            driver.find_element(By.CLASS_NAME, "btn-login").click()
            print("[DEBUG] Clicked login button")

            error_msg = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "message"))
            )
            print(f"[DEBUG] Error message received: {error_msg.text}")

            self.assertIn("Invalid credentials. Please try again.", error_msg.text)

        except Exception as e:
            print("[ERROR] Invalid password test failed")
            self.fail(str(e))

    def test_missing_email(self):
        """Test Case #3: Missing Email/Phone"""
        driver = self.driver
        try:
            print("[DEBUG] Testing missing email scenario...")

            driver.find_element(By.ID, "passwordInput").send_keys("12345")
            driver.find_element(By.CLASS_NAME, "btn-login").click()
            print("[DEBUG] Clicked login button")

            error_msg = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.ID, "message"))
            )
            print(f"[DEBUG] Error message received: {error_msg.text}")

            self.assertIn("Email/Phone", error_msg.text)

        except Exception as e:
            print("[ERROR] Missing email test failed")
            self.fail(str(e))

    def test_google_login(self):
        """Test Case #4: Google Login (Mock)"""
        driver = self.driver
        try:
            print("[DEBUG] Testing Google login...")

            google_iframe = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            print("[DEBUG] Google login iframe found")

            driver.switch_to.frame(google_iframe)
            google_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nsm7Bb-HzV7m-LgbsSe"))
            )
            print("[DEBUG] Google login button found")

            driver.execute_script("arguments[0].click();", google_button)
            print("[DEBUG] Clicked Google login button")

            driver.switch_to.default_content()
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(2)
            )

            main_window = driver.current_window_handle
            for handle in driver.window_handles:
                if handle != main_window:
                    driver.switch_to.window(handle)
                    break

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            print("[DEBUG] Google login popup detected.")

            driver.close()
            driver.switch_to.window(main_window)

            message_div = driver.find_element(By.ID, "message")
            print(f"[DEBUG] Login message: {message_div.text}")

            self.assertIn("Google sign-in successful", message_div.text)

        except Exception as e:
            print("[ERROR] Google login test failed")
            self.fail(str(e))

    def test_facebook_login(self):
        """Test Case #5: Facebook Login (Mock)"""
        driver = self.driver
        try:
            print("[DEBUG] Testing Facebook login...")

            facebook_button = driver.find_element(By.CLASS_NAME, "btn-facebook")
            print(f"[DEBUG] Facebook button displayed: {facebook_button.is_displayed()}")

            facebook_button.click()
            print("[DEBUG] Clicked Facebook login button")

            success_msg = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "message"))
            )
            print(f"[DEBUG] Facebook success message: {success_msg.text}")

            self.assertIn("Facebook sign-in successful", success_msg.text)

        except Exception as e:
            print("[ERROR] Facebook login test failed")

            self.fail(str(e))

if __name__ == "__main__":
    unittest.main()
