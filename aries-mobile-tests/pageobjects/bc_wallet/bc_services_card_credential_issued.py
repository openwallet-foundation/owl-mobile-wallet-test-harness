from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.information_sent_successfully import InformationSentSuccessfullyPage

class BCServicesCardCredentialIssuedPage(BasePage):
    """BC Services Card Credential Issued page object"""

    # Locators
    on_this_page_text_locator = "Your Credential has been Issued!"
    close_and_go_to_wallet_locator = (AppiumBy.ACCESSIBILITY_ID, "Close and go to wallet")


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_text_locator) 


    def close_and_go_to_wallet(self):
        if self.on_this_page():
            self.find_by(self.close_and_go_to_wallet_locator).click()
            return InformationSentSuccessfullyPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
