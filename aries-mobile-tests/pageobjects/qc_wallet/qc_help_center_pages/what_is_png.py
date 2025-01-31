from pageobjects.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class WhatIsPNGPageQC(BasePage):
    """what is PNG Info page object"""

    # Locators
    on_this_page_title_locator = "PNG"
    return_to_help_center_button_locator = (AppiumBy.ID, "com.ariesbifold:id/StartProcess")

    
    def on_this_page(self):
        # return self.find_by(self.on_this_page_title_locator) and self.find_by(self.on_this_page_text_locator)   
       return super().on_this_page(self.on_this_page_title_locator)
   
   
    def select_return(self):
        from pageobjects.qc_wallet.help import HelpPageQC 
        if self.on_this_page():
            self.find_by(self.return_to_help_center_button_locator).click()
            return HelpPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")