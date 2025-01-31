from pageobjects.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class WhatIsAPINPageQC(BasePage):
    """Secure your wallet What is a PIN Info page object"""
    
    en_title_text_locator = "PIN"
    fr_title_text_locator = "NIP"
    return_to_help_center_button_locator = (AppiumBy.ID, "com.ariesbifold:id/StartProcess")
    
    def __init__(self, driver):
        super().__init__(driver)
  
    def on_this_page(self):
        return super().on_this_page(self.en_title_text_locator) or super().on_this_page(self.fr_title_text_locator)
    
    
    def select_return(self):
        from pageobjects.qc_wallet.help import HelpPageQC 
        if self.on_this_page():
            self.find_by(self.return_to_help_center_button_locator).click()
            return HelpPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")