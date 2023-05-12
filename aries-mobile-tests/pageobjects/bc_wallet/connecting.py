import os
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
import logging
from selenium.common.exceptions import TimeoutException
from pageobjects.basepage import WaitCondition


# These classes can inherit from a BasePage to do common setup and functions
class ConnectingPage(BasePage):
    """Connecting to an Agent Screen page object"""

    # Locators
    on_this_page_text_locator = "Just a moment"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialOnTheWay")
    taking_too_long_locator =   (AppiumBy.ID, "com.ariesbifold:id/TakingTooLong")
    back_to_home_locator =  (AppiumBy.ID, "com.ariesbifold:id/BackToHome")

    def on_this_page(self):   
        timeout = 20
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 50 
        return super().on_this_page(self.on_this_page_locator, timeout)

    def select_go_back_to_home(self):
        if self.on_this_page():
            self.find_by(self.back_to_home_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def is_connecting_taking_too_long(self):
        if self.find_by(self.taking_too_long_locator, timeout=60, wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED):
            return True
        else:
            return False

    def wait_for_connection(self, timeout=300):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Wait for the Connection indicator to disappear
        try:
            self.find_by(self.on_this_page_locator, timeout, WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED)
            logger.debug("Connecting indicator disappeared")
        except TimeoutException:
            logger.error(f"Connecting taking longer than expected. Timing out at {timeout} seconds.")
            raise

        # Return the True if done connecting
        return True