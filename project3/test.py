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
        cls.server_process = subprocess.Popen(["python3", "-m", "http.server", "3000"])
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--lang=en-US")
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")
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
        time.sleep(2)
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
        driver.execute_script("document.documentElement.lang = 'en';")
        try:
            print("[DEBUG] Testing Google login...")
            google_button_xpath = "/html/body/div/div[3]/div[2]/div/div/div/div[2]"  # Replace with actual XPath
            google_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, google_button_xpath))
            )
            print("[DEBUG] Clicking Google login button")
            google_button.click()
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            main_window = driver.current_window_handle
            new_window = None
            for handle in driver.window_handles:
                if handle != main_window:
                    new_window = handle
                    break
            if new_window is None:
                raise AssertionError("[ERROR] Google login popup did not open!")
            driver.switch_to.window(new_window)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            print("[DEBUG] Google login popup detected.")
            email_input = driver.find_elements(By.XPATH, "//*[@id='identifierId']")
            email_input[0].send_keys("invalid_email@example.com")
            next_button_email_xpath = "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/div[3]"  # Correct XPath
            next_button_email = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, next_button_email_xpath))
            )
            current_url_before = driver.current_url
            print(f"[DEBUG] Current URL before login attempt: {current_url_before}")
            print("[DEBUG] Clicking the 'Next' button for email")
            driver.execute_script("arguments[0].click();", next_button_email)
            time.sleep(5)
            current_url_after = driver.current_url
            print(f"[DEBUG] Current URL after login attempt: {current_url_after}")
            self.assertEqual(current_url_before, current_url_after, "The page should not have changed!")
            driver.close()
            driver.switch_to.window(main_window)

        except Exception as e:
            print(f"[ERROR] Google login test failed: {e}")
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
    def test_invalid_characters(self):
        """Test Case #6: Invalid Characters (@@)"""
        driver = self.driver
        try:
            print("[DEBUG] Testing input with @@.")
            driver.find_element(By.ID, "emailInput").send_keys("test@@example.comñ")
            driver.find_element(By.ID, "passwordInput").send_keys("12345")
            driver.find_element(By.CLASS_NAME, "btn-login").click()
            print("[DEBUG] Clicked login button")
            success_msg = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "message"))
            )
            print(f"[DEBUG] Success message received: {success_msg.text}")
            self.assertIn("Login Successful", success_msg.text)
        except Exception as e:
            print("[ERROR] Invalid characters test failed")
            self.fail(str(e))
    def test_valid_standard_login_mobile(self):
        """Test Case #7: Valid Standard Login Using Mobile Phone Number"""
        driver = self.driver
        try:
            print("[DEBUG] Attempting standard login...")
            email_field = driver.find_element(By.ID, "emailInput")
            password_field = driver.find_element(By.ID, "passwordInput")
            login_button = driver.find_element(By.CLASS_NAME, "btn-login")
            print(f"[DEBUG] Email field displayed: {email_field.is_displayed()}")
            print(f"[DEBUG] Password field displayed: {password_field.is_displayed()}")
            print(f"[DEBUG] Login button displayed: {login_button.is_displayed()}")
            email_field.send_keys("5551234567")
            password_field.send_keys("phonePass")
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
if __name__ == "__main__":
    unittest.main()
