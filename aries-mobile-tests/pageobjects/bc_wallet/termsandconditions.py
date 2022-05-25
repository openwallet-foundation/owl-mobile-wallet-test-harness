import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.secure import SecurePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage


# These classes can inherit from a BasePage to do commone setup and functions
class TermsAndConditionsPage(BasePage):
    """Terms and Conditions page object"""

    # Locators
    # TODO: We could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    on_this_page_text_locator = "EULA"
    terms_and_conditions_accept_aid_locator = "I Agree"
    terms_and_conditions_accept_tid_locator = (MobileBy.ID, "com.ariesbifold:id/IAgree")
    continue_button_locator = (MobileBy.ID, "com.ariesbifold:id/Continue")
    continue_button_aid_locator = (MobileBy.ACCESSIBILITY_ID, "Continue")
    back_locator = (MobileBy.ID, "com.ariesbifold:id/Back")
    back_aid_locator = (MobileBy.ACCESSIBILITY_ID, "Back")


    def on_this_page(self):   
        #print(self.driver.page_source)     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_accept(self):
        if self.on_this_page():
            self.scroll_to_element(self.back_aid_locator[1])
            self.find_by(self.terms_and_conditions_accept_tid_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_continue(self):
        if self.on_this_page():
            self.scroll_to_element(self.back_aid_locator[1])
            self.find_by(self.continue_button_locator).click()

            # Maybe should check if it is checked or let the test call is_accept_checked()? 
            # return a new page object? The Pin Setup page.
            return PINSetupPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_back(self):
        if self.on_this_page():
            self.scroll_to_element(self.back_aid_locator[1])
            self.find_by(self.back_locator).click()
            # Returning BasePage here since they could of got here by skipping and they would return the the onboarding page
            # they selected skip on. Tests will have to track what onboarding page they were on in the tests and make sure they are there. 
            return BasePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")