import os
import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from pageobjects.bc_wallet.initialization import InitializationPage

class BiometricsPage(BasePage):
    """Biometrics enter page object"""

    # Locators
    on_this_page_text_locator = "Wallet Unlock"


    def on_this_page(self):   
        #print(self.driver.page_source)  
        timeout = 50
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 100
        return super().on_this_page(self.on_this_page_text_locator, timeout)  
