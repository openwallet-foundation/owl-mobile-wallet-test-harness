from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.credentials import CredentialsPage


# These classes can inherit from a BasePage to do common setup and functions
class CredentialAddedPage(BasePage):
    """Credential Added page object"""

    # Locators
    on_this_page_text_locator = "Credential added to your wallet"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialAddedToYourWallet")
    done_locator = (AppiumBy.ID, "com.ariesbifold:id/Done")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_locator)

    def select_done(self):
        if self.on_this_page():
            self.find_by(self.done_locator).click()
            return CredentialsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")