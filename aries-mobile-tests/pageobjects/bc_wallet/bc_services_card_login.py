import os
from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.bc_services_card_login_vt_csn import BCServicesCardLoginVTCSNPage
from pageobjects.bc_wallet.bc_services_card_login_unpw import BCServicesCardLoginUNPWPage

class BCServicesCardLoginPage(BasePage):
    """Create a BC Digitial ID web(internal to the app) page object"""

    # Locators
    on_this_page_text_locator = "BC Services Card Login"
    login_with_virtual_testing_locator = (AppiumBy.ACCESSIBILITY_ID, "Log in with Virtual testing")
    test_with_username_and_password_locator = (AppiumBy.ACCESSIBILITY_ID, "Log in with Test with username and password")


    def on_this_page(self):   
        timeout = 50
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 100
        return super().on_this_page(self.on_this_page_text_locator, timeout)  


    def select_virtual_testing(self):
        if self.on_this_page():
            self.find_by(self.login_with_virtual_testing_locator).click()
            return BCServicesCardLoginVTCSNPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_test_with_username_password(self):
        if self.on_this_page():
            self.find_by(self.test_with_username_and_password_locator).click()
            return BCServicesCardLoginUNPWPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
