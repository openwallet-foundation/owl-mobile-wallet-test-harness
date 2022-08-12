import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.initialization import InitializationPage

class PINPage(BasePage):
    """PIN Entry page object"""

    # Locators
    on_this_page_text_locator = "Enter PIN"
    pin_locator = (MobileBy.ID, "com.ariesbifold:id/EnterPIN")
    pin_visibility_locator = (MobileBy.ID, "com.ariesbifold:id/Show")
    enter_button_locator = (MobileBy.ID, "com.ariesbifold:id/Enter")

    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator, 50) 

    def enter_pin(self, pin):
        if self.on_this_page():
            self.find_by(self.pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_enter(self):
        if self.on_this_page():
            self.find_by(self.enter_button_locator).click()

            # return the wallet initialization page
            return InitializationPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page") 
