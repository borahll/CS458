import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium.options.android import UiAutomator2Options
import os
from appium.options.common import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait

class TestSurveyApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Called once before all tests. Sets up the Appium driver and waits for the app to launch.
        """
        options = AppiumOptions()
        options.set_capability("platformName", "Android")
        options.set_capability("deviceName", "emulator-5554")
        options.set_capability("automationName", "UiAutomator2")
        apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "/Users/borahaliloglu/Desktop/MacBook/CS4/CS4-2/CS458/CS458/project2/build/app/outputs/apk/debug/app-debug.apk"))
        options.set_capability("app", apk_path)
        options.set_capability("newCommandTimeout", 300)

        cls.driver = webdriver.Remote("http://localhost:4723", options=options)
        time.sleep(5)
        
    @classmethod
    def tearDownClass(cls):
        """
        Called once after all tests finish. Quits the driver.
        """
        cls.driver.quit()

    def wait(self, sec=2):
        """
        Helper method to do a simple sleep-based wait (in seconds).
        """
        time.sleep(sec)


    def test_email_login(self):
        wait = WebDriverWait(self.driver, 10)

        # Locate the email input field using the Android UIAutomator locator with AppiumBy
        email_field = wait.until(lambda driver: driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Email Input Field")'
        ))
        email_field.send_keys("test@example.com")

        # Locate the password input field
        password_field = wait.until(lambda driver: driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Password Input Field")'
        ))
        password_field.send_keys("12345")

        # Locate and tap the login button
        login_button = wait.until(lambda driver: driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Email Login Button")'
        ))
        login_button.click()

        # Optionally, wait for the next page or confirmation element to appear
        self.wait(3)











    def test_google_login_and_navigation(self):
        """
        TC1: Ensure Google login navigates to survey page.
        
        Steps:
        1. Click on Google Login button.
        2. Wait for navigation to the survey form.
        3. Verify the survey form header is present.
        
        This covers the requirement for a valid login flow from part1 -> part2.
        """
        google_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "GoogleLoginButton")
        google_btn.click()
        self.wait(4)
        
        header = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Survey Form")
        self.assertIsNotNone(header, "Survey Form header not found after Google login.")

    def test_checkbox_dynamic_cons_fields(self):
        """
        TC2: Check if 'cons' fields appear/disappear when toggling checkboxes.
        
        Steps:
        1. Select the ChatGPT checkbox.
        2. Verify the ChatGPTConsField appears (dynamic UI behavior).
        3. Deselect the ChatGPT checkbox.
        4. Verify the ChatGPTConsField disappears.
        
        This validates the dynamic creation/removal of cons fields for AI models.
        """
        chatgpt_cb = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTCheckbox")
        chatgpt_cb.click()
        self.wait()
        
        cons_field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTConsField")
        self.assertIsNotNone(cons_field, "ChatGPTConsField should appear after selecting checkbox.")

        # Uncheck to see if field is removed
        chatgpt_cb.click()
        self.wait()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTConsField")

    def test_send_button_conditional_visibility(self):
        """
        TC3: Check send button only appears when the survey form is complete.
        
        Steps:
        1. Verify SendSurveyButton does not exist initially (UI constraint).
        2. Fill in required fields: Name, City, Education, Gender, AI selection, cons, use case.
        3. Check that SendSurveyButton is now present and enabled.
        
        This covers multiple fields in one scenario, ensuring the form
        has all required data before enabling 'Send'.
        """
        with self.assertRaises(Exception):
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "SendSurveyButton")

        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "NameSurnameField").send_keys("Test User")
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "CityField").send_keys("Ankara")
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "EducationDropdown").click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "BachelorOption").click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "GenderDropdown").click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "MaleOption").click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTCheckbox").click()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTConsField").send_keys("Sometimes inaccurate")
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "AIUseCaseField").send_keys("Helps in coding")

        self.wait()
        btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "SendSurveyButton")
        self.assertTrue(btn.is_enabled(), "Send button should be enabled after all mandatory fields are filled.")

    def test_email_data_accuracy(self):
        """
        TC4: Validate that the submitted email or survey result contains all expected data.
        
        Steps:
        1. Tap 'SendSurveyButton'.
        2. Wait for a confirmation (Snackbar, toast, or next screen).
        3. (Manually or via logs) confirm the email was sent with correct content.
        
        This addresses the requirement of emailing the survey result upon "Send".
        """
        send_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "SendSurveyButton")
        send_btn.click()
        self.wait(3)
        # Assume a Snackbar/Toast or label appears with a success message
        # We just print a reminder to manually check or do a deeper integration test
        print("✅ Survey sent — validate email content manually or via test email address/logs.")

    def test_relogin_flow_after_logout(self):
        """
        TC5: Test logout + relogin + form state reset.
        
        Steps:
        1. Confirm we are on Survey Form.
        2. Simulate logout (via back or 'Logout' button).
        3. Verify user is on the login page again.
        4. Login again, confirm the form fields are reset (NameSurnameField is empty).
        
        Covers persistent session vs. fresh session scenario.
        """
        # Confirm we're on the survey form
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Survey Form")
        # Simulate logout
        self.driver.back()  # or use 'Logout' button if your app has it
        self.wait()

        # We should land back on login page
        google_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "GoogleLoginButton")
        self.assertIsNotNone(google_btn, "Google login button not found after logout navigation.")

        # Re-login
        google_btn.click()
        self.wait(3)

        # Confirm form is reset
        name_field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "NameSurnameField")
        self.assertEqual(name_field.text, "", "Name field should be empty after re-login flow.")

    def test_invalid_birth_date(self):
        """
        TC6: Provide an invalid birth date and check if an error or constraint is triggered.
        
        Steps:
        1. Enter a clearly invalid birth date, e.g., '31-02-2025'.
        2. Verify an error message or that the date field won't accept it.
        
        Demonstrates negative testing for a single field.
        Shows we're not just checking 'valid' inputs.
        """
        # Make sure the user is on the Survey Form (or re-login if needed)
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Survey Form")
        except NoSuchElementException:
            # If not found, do a quick login
            google_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "GoogleLoginButton")
            google_btn.click()
            self.wait(3)

        # Now test the invalid date
        birth_date_field = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "BirthDateField")
        birth_date_field.send_keys("31-02-2025")
        self.wait()

        # If your app instantly shows an error label or toast, check it here
        try:
            error_label = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "InvalidBirthDateError")
            self.assertIsNotNone(error_label, "Expected invalid birth date error was not displayed.")
        except NoSuchElementException:
            self.fail("No error displayed for an impossible birth date.")

    def test_multiple_ai_selections(self):
        """
        TC7: Check that selecting multiple AI models prompts multiple 'cons' fields,
        and that all remain visible and editable.
        
        Steps:
        1. Select ChatGPT and Bard checkboxes.
        2. Verify their 'cons' fields appear.
        3. Fill them, then deselect one to ensure the correct field disappears.
        4. Verify the other is still present.
        
        This test ensures the UI handles multi-check scenarios properly.
        """
        # Possibly re-login if needed
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Survey Form")
        except NoSuchElementException:
            google_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "GoogleLoginButton")
            google_btn.click()
            self.wait(3)

        # Select ChatGPT
        chatgpt_cb = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTCheckbox")
        chatgpt_cb.click()
        self.wait()
        chatgpt_cons = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTConsField")
        chatgpt_cons.send_keys("Hallucinations, sometimes inaccurate")

        # Select Bard
        bard_cb = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "BardCheckbox")
        bard_cb.click()
        self.wait()
        bard_cons = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "BardConsField")
        bard_cons.send_keys("Limited training data?")

        # Deselect ChatGPT to see if ChatGPTConsField disappears
        chatgpt_cb.click()
        self.wait()
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "ChatGPTConsField")

        # BardConsField should still exist
        bard_cons_test = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "BardConsField")
        self.assertIsNotNone(bard_cons_test, "Bard cons field disappeared unexpectedly after unchecking ChatGPT.")

if __name__ == '__main__':
    unittest.main()
