import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class AreYouSureDeclineProofRequestPage(BasePage):
    """Comfirm the decline of Proof Request page object"""

    # Locators
    on_this_page_text_locator = "Are you sure you want to decline this proof request"
    no_go_back_locator = (MobileBy.ID, "com.ariesbifold:id/Share")
    confirm_locator = (MobileBy.ID, "com.ariesbifold:id/Decline")


    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_confirm(self):
        if self.on_this_page():
            self.find_by(self.confirm_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_no_go_back(self):
        if self.on_this_page():
            self.find_by(self.no_go_back_locator).click()
            from pageobjects.bc_wallet.proof_request import ProofRequestPage
            return ProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

