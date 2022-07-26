import os
import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class ConnectingPage(BasePage):
    """Connecting to an Agent Screen page object"""

    # Locators
    on_this_page_text_locator = "Just a moment"
    on_this_page_locator = (MobileBy.ID, "com.ariesbifold:id/CredentialOnTheWay")
    back_to_home_locator = "Home"

    def on_this_page(self):   
        timeout = 10
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 50 
        return super().on_this_page(self.on_this_page_locator, timeout)

    def select_go_back_to_home(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.back_to_home_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")