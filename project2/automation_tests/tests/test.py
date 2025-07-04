import unittest
import time
import os
from appium import webdriver
from appium.options.common import AppiumOptions

from appium_flutter_finder import FlutterFinder, FlutterElement
from selenium.common.exceptions import NoSuchElementException


class TestSurveyApp(unittest.TestCase):

    def setUp(self):
        """
        Runs before each test method. 
        1) Launch new Appium driver
        2) Log in
        """
        options = AppiumOptions()
        options.set_capability("platformName", "Android")
        options.set_capability("deviceName", "emulator-5554")

        options.set_capability("automationName", "Flutter")

        apk_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../build/app/outputs/apk/debug/app-debug.apk"
            )
        )
        options.set_capability("app", apk_path)
        options.set_capability("newCommandTimeout", 300)

        self.driver = webdriver.Remote("http://localhost:4723", options=options)
        self.finder = FlutterFinder()
        time.sleep(5)  
        self.login_with_email()
        self.assertTrue(
            self.element_exists("Survey Form", 5),
            "Survey Form header not found after login!"
        )

    def tearDown(self):
        """
        Runs after each test method.
        Logs out (if desired) and quits the driver.
        """
        self.driver.quit()

    def wait(self, sec=2):
        """
        Helper to do a sleep-based wait (in seconds).
        """
        time.sleep(sec)
    def find_key(self, key_name):
        """
        Returns a FlutterElement for the given ValueKey name.
        """
        raw_finder = self.finder.by_value_key(key_name)
        return FlutterElement(self.driver, raw_finder)


    def element_exists(self, key_name, wait_seconds=3):

        """
        Returns True if the widget with the given ValueKey is found
        within `wait_seconds`, else False.
        """
        finder = self.finder.by_value_key(key_name)
        try:
            self.driver.execute_script("flutter: waitFor", finder, wait_seconds)
            return True
        except Exception:
            return False

    def element_absent(self, key_name, wait_seconds=3):
        """
        Returns True if the widget with the given ValueKey is gone
        (not found) within `wait_seconds`, else False.
        """
        finder = self.finder.by_value_key(key_name)
        try:
            self.driver.execute_script("flutter: waitForAbsent", finder, wait_seconds)
            return True
        except Exception:
            return False

    def login_with_email(self):
        """
        Helper method: fill email + password fields, and tap 'EmailLoginButton'
        """
        self.find_key("EmailField").send_keys("test@example.com")
  
        self.find_key("PasswordField").send_keys("12345")
        self.find_key("EmailLoginButton").click()
        self.wait(3)

    def test_login_and_navigation(self):
        """
        TC1: Already logged in (setUp did it).
        Just verify Survey Form is indeed visible.
        """
        self.assertTrue(
            self.element_exists("Survey Form"),
            "Survey Form header not found!"
        )

    def test_checkbox_dynamic_cons_fields(self):
        """
        TC2: Toggle ChatGPTCheckbox -> ChatGPTConsField appears/disappears.
        """
        self.find_key("ChatGPTCheckbox").click()
        self.wait()

        self.assertTrue(
            self.element_exists("ChatGPTConsField"),
            "ChatGPTConsField should appear after selecting ChatGPT."
        )

        self.find_key("ChatGPTCheckbox").click()
        self.wait()

        self.assertTrue(
            self.element_absent("ChatGPTConsField"),
            "ChatGPTConsField still exists after unchecking!"
        )

    def test_send_button_conditional_visibility(self):
        """
        TC3: 'SendSurveyButton' appears only after all required fields 
        (including valid manual date) are filled.
        """
        self.assertFalse(
            self.element_exists("SendSurveyButton", 2),
            "SendSurveyButton appeared prematurely!"
        )

        self.find_key("NameSurnameField").send_keys("Test User")
        self.find_key("CityField").send_keys("Ankara")

        self.find_key("BirthDateField").send_keys("02.04.2022")
        self.wait(1)

        self.find_key("EducationDropdown").click()
        self.find_key("BachelorOption").click()

        self.find_key("GenderDropdown").click()
        self.find_key("MaleOption").click()

        self.find_key("ChatGPTCheckbox").click()
        self.find_key("ChatGPTConsField").send_keys("Sometimes inaccurate")

        self.find_key("AIUseCaseField").send_keys("Helps in coding")
        self.wait()

        self.assertTrue(
            self.element_exists("SendSurveyButton", 3),
            "SendSurveyButton did not appear after filling required fields."
        )

    def test_email_data_accuracy(self):
        """
        TC4: Fill out form + click 'SendSurveyButton' -> Confirm success message/log, all fields should be filled.
        """
        self.find_key("NameSurnameField").send_keys("Tester")
        self.find_key("CityField").send_keys("Izmir")

        self.find_key("BirthDateField").send_keys("02.04.2023")
        self.wait(1)

        self.find_key("EducationDropdown").click()
        self.find_key("BachelorOption").click()

        self.find_key("GenderDropdown").click()
        self.find_key("FemaleOption").click()

        self.find_key("ChatGPTCheckbox").click()
        self.find_key("ChatGPTConsField").send_keys("Occasionally wrong")

        self.find_key("AIUseCaseField").send_keys("Project help")
        self.wait()

        self.find_key("SendSurveyButton").click()
        self.wait(3)

        print("Survey sent. Check logs or test email for result.")

    def test_incomplete_birth_date_format(self):
        """
        TC5: Typing an incomplete date (e.g. "01.01." => only 5 chars) 
             should keep the SendSurveyButton hidden.
        """
        
        self.find_key("NameSurnameField").send_keys("Incomplete Date Tester")
        self.find_key("CityField").send_keys("TestingTown")

        self.find_key("EducationDropdown").click()
        self.find_key("BachelorOption").click()

        self.find_key("GenderDropdown").click()
        self.find_key("MaleOption").click()

        self.find_key("ChatGPTCheckbox").click()
        self.find_key("ChatGPTConsField").send_keys("No date yet")

        self.find_key("AIUseCaseField").send_keys("Testing incomplete date")

        self.find_key("BirthDateField").send_keys("01.01.")
        self.wait(1)

        self.assertFalse(
            self.element_exists("SendSurveyButton", 2),
            "SendSurveyButton should NOT appear with incomplete date!"
        )

    def test_relogin_flow_after_logout(self):
        """
        TC6: If we want to test logout -> log in again in the same test
        """
        self.assertTrue(self.element_exists("Survey Form"))

        self.find_key("LogoutButton").click()
        self.wait()

        self.login_with_email()

    def test_multiple_ai_selections(self):
        """
        TC7: Select multiple AI checkboxes => multiple cons fields.
        """
        self.find_key("ChatGPTCheckbox").click()
        self.wait()
        self.find_key("ChatGPTConsField").send_keys("Hallucinations")

        self.find_key("BardCheckbox").click()
        self.wait()
        self.find_key("BardConsField").send_keys("Still developing")

        self.find_key("ChatGPTCheckbox").click()
        self.wait()
        self.assertFalse(
            self.element_exists("ChatGPTConsField"),
            "ChatGPTConsField is still present after unchecking ChatGPT!"
        )
        self.assertTrue(
            self.element_exists("BardConsField"),
            "BardConsField is missing after unchecking ChatGPT!"
        )

    def test_invalid_login(self):
        """
        TC8: Attempts to log in with invalid email/password -> 
        Confirm error message and that we don't navigate to Survey Form.
        """
        self.find_key("LogoutButton").click()
        self.find_key("EmailField").send_keys("wrong@example.com")
        self.find_key("PasswordField").send_keys("badpassword")

        self.find_key("EmailLoginButton").click()
        self.wait(1) 
        self.assertFalse(
            self.element_exists("Survey Form", wait_seconds=2),
            "Survey Form should NOT appear after invalid credentials!"
        )

if __name__ == '__main__':
    unittest.main()
