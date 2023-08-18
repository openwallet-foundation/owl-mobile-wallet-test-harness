import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.contact_details import ContactDetailsPage
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from selenium.common.exceptions import TimeoutException


class ContactPage(BasePage):
    """Contact page object"""

    # Locator
    on_this_page_text_locator = "Contacts"
    contact_locator = (AppiumBy.ID, "com.ariesbifold:id/Settings")
    chat_box_locator = (AppiumBy.ID, "com.ariesbifold:id/ChatBox")
    send_message_locator = (AppiumBy.ID, "com.ariesbifold:id/SendMessage")
    credential_offer_message_locator = (AppiumBy.XPATH, '//*[contains(@accessibilityId, "sent a credential offer")]')
    proof_request_message_locator = (AppiumBy.XPATH, '//*[contains(@accessibilityId, "sent a proof request")]')
    open_credential_offer_locator = (AppiumBy.ID, "com.ariesbifold:id/Viewoffer")
    open_proof_request_locator = (AppiumBy.ID, "com.ariesbifold:id/Viewrequest")

    def on_this_page(self):     
        return super().on_this_page(self.contact_locator) 

    def select_info(self):
        if self.on_this_page():
            self.find_by(self.contact_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

            # return a new page object for the Contacts page
            return ContactDetailsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}") 

    def select_open_credential_offer(self):
        if self.on_this_page():
            self.find_by(self.open_credential_offer_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")
    
    def select_open_proof_request(self):
        if self.on_this_page():
            self.find_by(self.open_proof_request_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return ProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}")

    def wait_for_credential_offer(self, timeout=300):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Wait for the credential offer to appear
        try:
            self.find_by(self.credential_offer_message_locator, timeout, WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)
            logger.debug("Credential Offer Appeared")
        except TimeoutException:
            logger.error(f"Credential Offer taking longer than expected. Timing out at {timeout} seconds.")
            raise

        # Return the True the credential offer appeared
        return True

    def wait_for_proof_request(self, timeout=300):
        # Set up logging
        logger = logging.getLogger(__name__)

        # Wait for the proof request to appear
        try:
            self.find_by(self.proof_request_message_locator, timeout, WaitCondition.PRESENCE_OF_ELEMENT_LOCATED)
            logger.debug("Proof Request Appeared")
        except TimeoutException:
            logger.error(f"Proof Request taking longer than expected. Timing out at {timeout} seconds.")
            raise

        # Return the True the proof request appeared
        return True