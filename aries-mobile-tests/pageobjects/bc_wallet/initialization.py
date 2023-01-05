from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import logging
from selenium.common.exceptions import TimeoutException
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.home import HomePage
import time


# These classes can inherit from a BasePage to do common setup and functions
class InitializationPage(BasePage):
    """Wallet initialization page that appears after setting up pin or entering pin"""

    # Locators
    #on_this_page_text_locator = (MobileBy.ID, "com.ariesbifold:id/LoadingActivityIndicator")
    loading_locator = (AppiumBy.ID, "com.ariesbifold:id/LoadingActivityIndicator")

    def on_this_page(self):
        #return super().on_this_page(self.on_this_page_text_locator)
        #print(self.driver.page_source)
        return self.still_initializing()

    def still_initializing(self):
        try:
            self.find_by(self.loading_locator)
            return True
        except:
            return False


    def wait_until_initialized(self, timeout=300):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Wait for the loading indicator to disappear
        try:
            self.find_by(self.loading_locator, timeout, WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED)
            logger.debug("Loading indicator disappeared")
        except TimeoutException:
            logger.error(f"App Initialization taking longer than expected. Timing out at {timeout} seconds.")
            raise

        # Check for the presence of an error message
        # if self.is_element_present(self.error_message_locator):
        #     error_message = self.find_by(self.error_message_locator).text
        #     logger.error(f"Error message found: {error_message}")
        #     raise Exception(f"Error occurred during app initialization: {error_message}")

        # Return the HomePage object
        return HomePage(self.driver)
