import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.allownotifications import AllowNotificationsPage

# These classes can inherit from a BasePage to do commone setup and functions
class SecurePage(BasePage):
    """Secure your wallet page object"""

    # Locators
    # TODO: We could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    on_this_page_text_locator = "Secure your Wallet"
    device_security_settings_link_locator = "device security settings"
    use_device_security_button_locator = "Submit"
    back_locator = "Back"

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_device_security_settings(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.device_security_settings_link_locator).click()
            # Not yet sure what to do here.
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_use_device_security(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.use_device_security_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return AllowNotificationsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_back(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.back_locator).click()
            return TermsAndConditionsPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page")