import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class ProofRequestDetailsPage(BasePage):
    """Proof Request Details page object"""
    
    # Locators
    on_this_page_text_locator = "which you can provide from:"
    back_locator = (MobileBy.ID, "com.ariesbifold:id/back")
    credential_locator = (MobileBy.ID, "com.ariesbifold:id/AttributeName")


    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.bc_wallet.proof_request import ProofRequestPage
            return ProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_first_credential_details(self):
        if self.on_this_page():
            credential_elements = self.find_multiple_by(self.credential_locator)
            return credential_elements[0].text
        else:
            raise Exception(f"App not on the {type(self)} page")
