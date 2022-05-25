import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.initialization import InitializationPage

class PINSetupPage(BasePage):
    """PIN Setup page object"""

    # Locators
    on_this_page_text_locator = "Enter Pin"
    first_pin_aid_locator = "Enter Pin"
    first_pin_tid_locator = "com.ariesbifold:id/EnterPin"
    second_pin_aid_locator = "Re-Enter Pin"
    second_pin_tid_locator = "com.ariesbifold:id/ReenterPin"
    create_pin_button_aid_locator = "Create"
    create_pin_button_tid_locator = "com.ariesbifold:id/Create"

    def on_this_page(self):   
        #print(self.driver.page_source)  
        return super().on_this_page(self.on_this_page_text_locator) 

    def enter_pin(self, pin):
        if self.on_this_page():
            self.find_by_element_id(self.first_pin_tid_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_pin(self):
        if self.on_this_page():
            return self.find_by_element_id(self.first_pin_tid_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_second_pin(self, pin):
        if self.on_this_page():
            self.find_by_element_id(self.second_pin_tid_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_second_pin(self):
        if self.on_this_page():
            return self.find_by_element_id(self.second_pin_tid_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")

    def create_pin(self):
        if self.on_this_page():
            self.find_by_element_id(self.create_pin_button_tid_locator).click()

            # return the wallet initialization page
            return InitializationPage(self.driver)
            #return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page") 
