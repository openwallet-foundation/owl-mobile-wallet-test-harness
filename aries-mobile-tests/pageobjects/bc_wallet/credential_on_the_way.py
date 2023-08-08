from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.credential_added import CredentialAddedPage
import logging
from selenium.common.exceptions import TimeoutException
from pageobjects.basepage import WaitCondition


# These classes can inherit from a BasePage to do common setup and functions
class CredentialOnTheWayPage(BasePage):
    """Credential is on its way page object"""

    # Locators
    on_this_page_text_locator = "Your credential is on the way"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialOnTheWay")
    home_locator = (AppiumBy.ID, "com.ariesbifold:id/BackToHome")


    def __init__(self, driver):
        super().__init__(driver)
        # Instantiate possible Modals and Alerts for this page
        self.unable_to_accept_credential_offer_modal = UnableToAcceptCredentialOfferModal(driver)

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_locator)

    def select_home(self):
        if self.on_this_page():
            self.find_by(self.home_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def wait_for_credential(self, timeout=300):

        # Wait for the Credential On the way indicator to disappear
        try:
            # Make sure the unable to accept credential offer modal is not displayed
            if not self.unable_to_accept_credential_offer_modal.is_displayed():
                self.find_by(self.on_this_page_locator, timeout, WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED)
                logging.debug("Credential On the way indicator disappeared")
            else:
                self.raise_exception_unable_to_accept_credential_offer()
        except TimeoutException:
            logging.error(f"Getting Credential taking longer than expected. Timing out at {timeout} seconds.")
            # Check if the unable to accept credential offer modal is displayed
            if self.unable_to_accept_credential_offer_modal.is_displayed():
                self.raise_exception_unable_to_accept_credential_offer()
            raise

        # Return the HomePage object
        return CredentialAddedPage(self.driver)

    def raise_exception_unable_to_accept_credential_offer(self):
        # Get the main error
        main_error = self.unable_to_accept_credential_offer_modal.get_main_error()
        # Get the detailed error
        self.unable_to_accept_credential_offer_modal.select_show_details()
        detailed_error = self.unable_to_accept_credential_offer_modal.get_detailed_error()
        # Select Okay
        self.unable_to_accept_credential_offer_modal.select_okay()
        # Raise an exception
        raise Exception(f"Unable to accept credential offer. Main Error: {main_error}. Detailed Error: {detailed_error}")

class UnableToAcceptCredentialOfferModal(BasePage):
    """Unable to Accept Credential Offer Modal page object"""

    # Locators
    on_this_page_text_locator = "Unable to accept credential offer."
    error_locator = (AppiumBy.ID, "com.ariesbifold:id/BodyText")
    show_details_locator = (AppiumBy.ID, "com.ariesbifold:id/ShowDetails")
    okay_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay") 

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)
    
    def is_displayed(self):
        return self.on_this_page()

    def get_main_error(self) -> str:
        return self.find_by(self.error_locator).text
        
    def select_show_details(self):
        self.find_by(self.show_details_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

    def get_detailed_error(self) -> str:
        return self.find_by(self.error_locator).text

    def select_okay(self):
        self.find_by(self.okay_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

