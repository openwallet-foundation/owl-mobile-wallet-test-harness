import os
from pageobjects.basepage import BasePage

class BiometricsPage(BasePage):
    """Biometrics enter page object"""

    # Locators
    on_this_page_text_locator = "Wallet Unlock"


    def on_this_page(self, language = "English"):   
        #print(self.driver.page_source)  
        self.on_this_page_text_locator = "Wallet Unlock" if language == "English" else "Déverrouillage du portefeuille"
        timeout = 50
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 100
        return super().on_this_page(self.on_this_page_text_locator, timeout)  
