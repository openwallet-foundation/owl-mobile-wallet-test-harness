import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.secure import SecurePage

# These classes can inherit from a BasePage to do commone setup and functions
class TermsAndConditionsPage(BasePage):
    """Terms and Conditions page object"""

    # Locators
    # TODO: We could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    on_this_page_text_locator = "EULA"
    terms_and_conditions_accept_locator = "I Agree to the Terms of Service"
    continue_button_locator = "Submit"
    back_locator = "Back"


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_accept(self):
        if self.on_this_page():
            self.driver.swipe(500, 2000, 500, 100)
            self.find_by_accessibility_id(self.terms_and_conditions_accept_locator).click()
            return True
        else:
            raise Exception(f"App not on the {self.on_this_page_text_locator} page")


    def select_continue(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.continue_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return SecurePage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page")


    def select_back(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.back_locator).click()
            # not sure what page to return here since they could of got here by skipping and they would return the the onboarding page
            # they selected skip on.
            return BasePage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page")