import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bifold.home import HomePage

class PINSetupPage(BasePage):
    """PIN Setup page object"""

    # Locators
    title_locator = "PIN"
    first_pin_locator = "Enter Pin"
    second_pin_locator = "Re-Enter Pin"
    create_pin_button_locator = "Create"

    def enter_pin(self, pin):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.first_pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {self.title_locator} page")

    def enter_second_pin(self, pin):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.second_pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {self.title_locator} page")

    def create_pin(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.create_pin_button_locator).click()

            # return a new page object? The Home page.
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page") 
