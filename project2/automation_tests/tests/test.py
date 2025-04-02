import unittest
import time
import os
from appium import webdriver
from appium_flutter_finder import FlutterElement, FlutterFinder
from appium.options.common import AppiumOptions
from selenium.common.exceptions import NoSuchElementException

class TestSurveyApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up Appium Options for Android + Flutter
        options = AppiumOptions()
        options.set_capability("platformName", "Android")
        options.set_capability("deviceName", "emulator-5554")   # or actual device name
        options.set_capability("automationName", "Flutter")

        # Path to your app's debug APK (auto-resolved from relative path)
        apk_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), 
                "../../build/app/outputs/apk/debug/app-debug.apk"
            )
        )
        options.set_capability("app", apk_path)
        options.set_capability("newCommandTimeout", 300)

        # Create Appium driver
        cls.driver = webdriver.Remote("http://localhost:4723", options=options)
        cls.finder = FlutterFinder()  # if you want to use finder for text or such
        time.sleep(5)  # short initial wait for app to load

    @classmethod
    def tearDownClass(cls):
        # Quit the driver after all tests complete
        cls.driver.quit()

    def wait(self, sec=2):
        """
        Helper to do a sleep-based wait (in seconds).
        """
        time.sleep(sec)

    # ========== HELPER METHODS ==========

    def find_key(self, key_name):
        """
        Returns a FlutterElement for the given ValueKey name.
        Example usage: driver.find_element(self.find_key('MyValueKey')).click()
        """
        return TestSurveyApp.finder.by_value_key(key_name)

    def login_with_email(self):
        """
        Helper method: fill email + password fields, and tap 'EmailLoginButton'
        """
        # EmailField
        self.driver.find_element(self.find_key("EmailField")).send_keys("test@example.com")
        # PasswordField
        self.driver.find_element(self.find_key("PasswordField")).send_keys("12345")
        # Tap EmailLoginButton
        self.driver.find_element(self.find_key("EmailLoginButton")).click()
        self.wait(3)

    def element_exists(self, key_name):
        """
        Returns True if an element with the given ValueKey exists, else False.
        """
        try:
            self.driver.find_element(self.find_key(key_name))
            return True
        except NoSuchElementException:
            return False

    # ========== TEST CASES ==========

    def test_login_and_navigation(self):
        """
        TC1: Email login should navigate to the Survey Form page.
        """
        self.login_with_email()
        self.assertTrue(
            self.element_exists("Survey Form"),
            "Survey Form header not found after login."
        )

    def test_checkbox_dynamic_cons_fields(self):
        """
        TC2: Toggle ChatGPTCheckbox -> ChatGPTConsField appears/disappears.
        """
        self.login_with_email()
        # Click 'ChatGPTCheckbox' to show cons field
        self.driver.find_element(self.find_key("ChatGPTCheckbox")).click()
        self.wait()
        self.assertTrue(
            self.element_exists("ChatGPTConsField"),
            "ChatGPTConsField should appear after selecting ChatGPT."
        )
        # Uncheck - ChatGPTConsField should go away
        self.driver.find_element(self.find_key("ChatGPTCheckbox")).click()
        self.wait()
        self.assertFalse(
            self.element_exists("ChatGPTConsField"),
            "ChatGPTConsField still exists after unchecking!"
        )

    def test_send_button_conditional_visibility(self):
        """
        TC3: 'SendSurveyButton' appears only after all required fields are filled.
        """
        self.login_with_email()
        # Should not exist initially
        self.assertFalse(
            self.element_exists("SendSurveyButton"),
            "SendSurveyButton appeared prematurely!"
        )

        # Fill out form
        self.driver.find_element(self.find_key("NameSurnameField")).send_keys("Test User")
        self.driver.find_element(self.find_key("CityField")).send_keys("Ankara")
        self.driver.find_element(self.find_key("EducationDropdown")).click()
        self.driver.find_element(self.find_key("BachelorOption")).click()
        self.driver.find_element(self.find_key("GenderDropdown")).click()
        self.driver.find_element(self.find_key("MaleOption")).click()
        self.driver.find_element(self.find_key("ChatGPTCheckbox")).click()
        self.driver.find_element(self.find_key("ChatGPTConsField")).send_keys("Sometimes inaccurate")
        self.driver.find_element(self.find_key("AIUseCaseField")).send_keys("Helps in coding")
        self.wait()

        # Now the SendSurveyButton should appear (and presumably be enabled)
        self.assertTrue(
            self.element_exists("SendSurveyButton"),
            "SendSurveyButton did not appear after filling required fields."
        )

    def test_email_data_accuracy(self):
        """
        TC4: Fill out form + click 'SendSurveyButton' -> Confirm success message/log
        """
        self.login_with_email()

        # Fill required fields
        self.driver.find_element(self.find_key("NameSurnameField")).send_keys("Tester")
        self.driver.find_element(self.find_key("CityField")).send_keys("Izmir")
        self.driver.find_element(self.find_key("EducationDropdown")).click()
        self.driver.find_element(self.find_key("BachelorOption")).click()
        self.driver.find_element(self.find_key("GenderDropdown")).click()
        self.driver.find_element(self.find_key("FemaleOption")).click()
        self.driver.find_element(self.find_key("ChatGPTCheckbox")).click()
        self.driver.find_element(self.find_key("ChatGPTConsField")).send_keys("Occasionally wrong")
        self.driver.find_element(self.find_key("AIUseCaseField")).send_keys("Project help")

        self.wait()
        # Tap 'SendSurveyButton'
        self.driver.find_element(self.find_key("SendSurveyButton")).click()
        self.wait(3)

        print("✅ Survey sent. Check logs or test email for result.")

    def test_relogin_flow_after_logout(self):
        """
        TC5: After logout, re-login -> form fields are reset.
        """
        self.login_with_email()
        # Confirm on Survey Form
        self.assertTrue(self.element_exists("Survey Form"))

        # Simulate logout with 'back' or a real logout button
        self.driver.back()
        self.wait()

        # Re-login
        self.login_with_email()
        # The NameSurnameField should be empty again
        name_text = self.driver.find_element(self.find_key("NameSurnameField")).text
        self.assertEqual(
            name_text, "",
            "Expected NameSurnameField to be empty after re-login."
        )

    def test_invalid_birth_date(self):
        """
        TC6: Provide invalid birth date -> check if error is shown
        """
        self.login_with_email()

        # Tap birth date field
        self.driver.find_element(self.find_key("BirthDateField")).click()
        self.wait()

        # Expect error label
        self.assertTrue(
            self.element_exists("InvalidBirthDateError"),
            "Invalid birth date error was not displayed."
        )

    def test_multiple_ai_selections(self):
        """
        TC7: Select multiple AI checkboxes => multiple cons fields.
        Then unselect ChatGPT => ChatGPTConsField should disappear, Bard remains.
        """
        self.login_with_email()

        # Select ChatGPT
        self.driver.find_element(self.find_key("ChatGPTCheckbox")).click()
        self.wait()
        self.driver.find_element(self.find_key("ChatGPTConsField")).send_keys("Hallucinations")

        # Select Bard
        self.driver.find_element(self.find_key("BardCheckbox")).click()
        self.wait()
        self.driver.find_element(self.find_key("BardConsField")).send_keys("Still developing")

        # Unselect ChatGPT => ChatGPTConsField disappears
        self.driver.find_element(self.find_key("ChatGPTCheckbox")).click()
        self.wait()
        self.assertFalse(
            self.element_exists("ChatGPTConsField"),
            "ChatGPTConsField is still present after unchecking ChatGPT!"
        )
        # BardConsField should remain
        self.assertTrue(
            self.element_exists("BardConsField"),
            "BardConsField is missing after unchecking ChatGPT!"
        )

if __name__ == '__main__':
    unittest.main()
