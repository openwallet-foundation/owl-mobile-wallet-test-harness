import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboardingstorecredssecurely import OnboardingStoreCredsSecurelyPage

# These classes can inherit from a BasePage to do common setup and functions
class OnboardingWelcomePage(BasePage):
    """Onboarding Welcome Screen page object"""

    # Locators
    # TODO: If Ontario/BC or other wallets are closely alligned and only locators are different, 
    # we could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    title_locator = "Welcome"
    page_text_locator = "Page Text"
    next_locator = "Next"
    skip_locator = "Skip"

    def get_onboarding_text(self):
        if self.on_the_right_page(self.title_locator):
            pass
        else:
            raise Exception(f"App not on the {self.title_locator} page")

    def select_next(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.next_locator).click()
            return OnboardingStoreCredsSecurelyPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page")

    def select_skip(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.skip_locator).click()
            return OnboardingStoreCredsSecurelyPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page")