import os
from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.bc_services_card_login import BCServicesCardLoginPage

class CreateABCDigitalIDPage(BasePage):
    """Create a BC Digitial ID web(internal to the app) page object"""

    # Locators
    on_this_page_text_locator = "Create a Person credential"
    log_in_with_bc_services_card_locator = (AppiumBy.ACCESSIBILITY_ID, "Log in with BC Services Card")


    def on_this_page(self):   
        timeout = 50
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 100
        return super().on_this_page(self.on_this_page_text_locator, timeout)  


    def select_login_with_bc_services_card(self):
        if self.on_this_page():
            self.find_by(self.log_in_with_bc_services_card_locator).click()
            return BCServicesCardLoginPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
