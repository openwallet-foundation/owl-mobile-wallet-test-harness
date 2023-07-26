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
        # Set up logging
        logger = logging.getLogger(__name__)

        # Wait for the Credential On the way indicator to disappear
        try:
            self.find_by(self.on_this_page_locator, timeout, WaitCondition.INVISIBILITY_OF_ELEMENT_LOCATED)
            logger.debug("Credential On the way indicator disappeared")
        except TimeoutException:
            logger.error(f"App Initialization taking longer than expected. Timing out at {timeout} seconds.")
            raise

        # Return the HomePage object
        return CredentialAddedPage(self.driver)

    # def select_cancel(self):
    #     if self.on_this_page():
    #         self.find_by_accessibility_id(self.cancel_locator).click()
    #         from pageobjects.bc_wallet.home import HomePage
    #         return HomePage(self.driver)
    #     else:
    #         raise Exception(f"App not on the {type(self)} page")
