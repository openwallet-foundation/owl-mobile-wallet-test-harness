import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.proof_request_declined import ProofRequestDeclinedPage


# These classes can inherit from a BasePage to do common setup and functions
class AreYouSureDeclineProofRequestPage(BasePage):
    """Comfirm the decline of Proof Request page object"""

    # Locators
    on_this_page_text_locator = "Are you sure you want to decline this proof request"
    no_go_back_locator = (AppiumBy.ID, "com.ariesbifold:id/AbortDeclineButton")
    confirm_locator = (AppiumBy.ID, "com.ariesbifold:id/ConfirmDeclineButton")


    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_confirm(self):
        if self.on_this_page():
            self.find_by(self.confirm_locator).click()
            return ProofRequestDeclinedPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_no_go_back(self):
        if self.on_this_page():
            self.find_by(self.no_go_back_locator).click()
            from pageobjects.bc_wallet.proof_request import ProofRequestPage
            return ProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

