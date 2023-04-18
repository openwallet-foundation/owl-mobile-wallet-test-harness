from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.bc_wallet.home import HomePage


# These classes can inherit from a BasePage to do common setup and functions
class CredentialDeclinedPage(BasePage):
    """Credential Declined page object"""

    # Locators
    on_this_page_text_locator = "Credential Declined"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/RequestOrOfferDeclined")
    done_locator = (AppiumBy.ID, "com.ariesbifold:id/Done")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_locator)

    def select_done(self):
        if self.on_this_page():
            self.find_by(self.done_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
