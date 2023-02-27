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
    error_intializing_locator = (AppiumBy.ID, "com.ariesbifold:id/HeaderText")
    error_message_locator = (AppiumBy.ID, "com.ariesbifold:id/BodyText")
    error_details_link_locator = (AppiumBy.ID, "com.ariesbifold:id/ShowDetails") 
    error_details_locator = (AppiumBy.ID, "com.ariesbifold:id/DetailsText")
    error_okay_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay")

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


    def wait_until_initialized(self, timeout=100):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Wait for the loading indicator to disappear
        try:
            self.find_by(self.loading_locator, timeout, WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED)
            logger.debug("Loading indicator disappeared")
        except TimeoutException:
            # TODO add in a check for the timeout error message from the app. 
            logger.error(f"App Initialization taking longer than expected. Timing out at {timeout} seconds.")
            logger.error(f"Checking Initialization for error...")
            if self.find_by(self.error_intializing_locator):
                error_title = self.find_by(self.error_intializing_locator).text
                error_message = self.find_by(self.error_message_locator).text
                self.find_by(self.error_details_link_locator).click()
                error_details = self.find_by(self.error_message_locator).text
                logger.error(f"BC Wallet Error: {error_title}\n{error_message}\n{error_details}")
                self.find_by(self.error_okay_button_locator).click()
                # not sure what to do after this? Should I try and restart the app?
                #raise Exception(f"Error occurred during app initialization: {error_message}")
            raise

        # Return the HomePage object
        return HomePage(self.driver)
