import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.home import HomePage
#from pageobjects.bc_wallet.secure import SecurePage

# These classes can inherit from a BasePage to do commone setup and functions
class AllowNotificationsPage(BasePage):
    """Allow Notifications page object"""

    # Locators
    # TODO: We could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    title_locator = "Allow notifications"
    continue_button_locator = "Continue"
    skip_for_now_button_locator = "Skip for now"
    back_locator = "Back"


    def select_continue(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.continue_button_locator).click()
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_skip_for_now(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.skip_for_now_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_back(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.back_locator).click()
            from pageobjects.bc_wallet.secure import SecurePage
            return SecurePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")