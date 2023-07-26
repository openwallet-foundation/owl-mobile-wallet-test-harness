import os
import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from pageobjects.bc_wallet.initialization import InitializationPage

class ToastNotification(BasePage):
    """base class for the toast notification page object"""

    # Locators
    on_this_page_text_locator:str
    notification_locator:tuple

    def on_this_page(self):   
        timeout = 50
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 100
        return super().on_this_page(self.on_this_page_text_locator, timeout)  

    def dismiss_notification(self):
        if self.on_this_page():
            self.find_by(self.notification_locator).click()
            # Not sure what is returned here yet
            # return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
