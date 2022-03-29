import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
#from pageobjects.bc_wallet.credentials import CredentialsPage
#from pageobjects.bc_wallet.home import HomePage


# These classes can inherit from a BasePage to do common setup and functions
class CredentialsPage(BasePage):
    """Credentials page object"""

    # Locators
    on_this_page_text_locator = "Credential added to your wallet"
    credential_locator = "credential"

    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def get_credentials(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.credential_locator).click()
            return #credentials list
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_latest_credential(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.credential_locator).click()
            return #credential
        else:
            raise Exception(f"App not on the {type(self)} page")

    def credential_exists(self, cred_name):
        return cred_name in self.driver.page_source