from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import logging
from selenium.common.exceptions import TimeoutException
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
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

    def __init__(self, driver):
        super().__init__(driver)
        # Instantiate possible Modals and Alerts for this page
        self.oops_something_went_wrong_modal = OopsSomethingWentWrongModal(driver)

    def on_this_page(self):
        return self.still_initializing()

    def still_initializing(self):
        # Check for something went wrong modal
        if self.oops_something_went_wrong_modal.is_displayed():
            # Get the main error
            main_error = self.oops_something_went_wrong_modal.get_main_error()
            # if Timeout error, then raise exception
            if self.oops_something_went_wrong_modal.is_timeout_error():
                raise Exception(main_error)
            else:
                # Otherwise, Show details, and get the details message and raise exception
                self.oops_something_went_wrong_modal.select_show_details()
                detailed_error = self.oops_something_went_wrong_modal.get_detailed_error()
                raise Exception(f"{main_error}\n{detailed_error}")
        try:
            self.find_by(self.loading_locator)
            return True
        except:
            return False


    def wait_until_initialized(self, timeout=100, retry_attempts=3):
        logger = logging.getLogger(__name__)

        for i in range(retry_attempts):
            try:
                if self.still_initializing():
                    self.find_by(self.loading_locator, timeout, WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED)
                    logger.debug("Loading indicator disappeared")
                else:
                    from pageobjects.bc_wallet.home import HomePage
                    return HomePage(self.driver)
            except TimeoutException:
                try:
                    self.still_initializing()
                except Exception as e:
                    if "Oops! Something went wrong" in str(e):
                        logger.error(f"Oops! Something went wrong. {e}")
                        self.oops_something_went_wrong_modal.select_retry()
                    else:
                        raise
            except Exception as e:
                if "Oops! Something went wrong" in str(e):
                    logger.error(f"Oops! Something went wrong. {e}")
                    self.oops_something_went_wrong_modal.select_retry()
                else:
                    raise
        return HomePage(self.driver)

class OopsSomethingWentWrongModal(BasePage):
    """Oops! Something went wrong Modal page object"""

    # Locators
    on_this_page_text_locator = "Oops! Something went wrong"
    main_error_locator = (AppiumBy.ID, "com.ariesbifold:id/BodyText")
    show_details_locator = (AppiumBy.ID, "com.ariesbifold:id/ShowDetails")
    detailed_error_locator = (AppiumBy.ID, "com.ariesbifold:id/DetailsText")
    retry_locator = (AppiumBy.ID, "com.ariesbifold:id/Retry")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)
    
    def is_displayed(self):
        return self.on_this_page()
    
    def is_timeout_error(self):
        return "Timeout" in self.get_main_error()

    def get_main_error(self) -> str:
        return self.find_by(self.main_error_locator).text
        
    def select_show_details(self):
        self.find_by(self.show_details_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

    def get_detailed_error(self) -> str:
        return self.find_by(self.detailed_error_locator).text

    def select_retry(self):
        self.find_by(self.okay_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

