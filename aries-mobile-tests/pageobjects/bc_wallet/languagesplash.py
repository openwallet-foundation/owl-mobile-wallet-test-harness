import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboardingwelcome import OnboardingWelcomePage

# These classes can inherit from a BasePage to do common setup and functions
class LanguageSplashPage(BasePage):
    """Set Language Spash Screen page object - Out Of Scope"""

    # Locators
    # TODO: If Ontario/BC or other wallets are closely alligned and only locators are different, 
    # we could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    title_locator = "British Columbia"
    bc_splash_image_locator = "British Columbia"
    english_button_locator = "English"
    french_button_locator = "French"

    def on_this_page(self):
        if self.on_the_right_page(self.title_locator):
            return True
        else:
            return False

    def select_english(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.english_button_locator).click()
            return OnboardingWelcomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_french(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.french_button_locator).click()
            return OnboardingWelcomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")