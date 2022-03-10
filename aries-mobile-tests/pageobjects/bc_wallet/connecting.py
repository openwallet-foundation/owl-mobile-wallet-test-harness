import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class ConnectingPage(BasePage):
    """Connecting to an Agent Screen page object"""

    # Locators
    on_this_page_text_locator = "Just a moment while we make a secure connection"
    back_to_home_locator = "Go back to home"

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator)   

    def select_go_back_to_home(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.back_to_home_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")