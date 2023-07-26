from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class DeclineCredentialOfferPage(BasePage):
    """Comfirm the decline of a Credential Offer page object"""

    # Locators
    on_this_page_text_locator = "Decline credential offer?"
    no_go_back_locator = (AppiumBy.ID, "com.ariesbifold:id/CancelDeclineButton")
    confirm_locator = (AppiumBy.ID, "com.ariesbifold:id/ConfirmDeclineButton")


    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_decline(self):
        if self.on_this_page():
            self.find_by(self.confirm_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_no_go_back(self):
        if self.on_this_page():
            self.find_by(self.no_go_back_locator).click()
            from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
            return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

