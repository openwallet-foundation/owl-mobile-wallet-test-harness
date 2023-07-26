from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.bc_services_card_credential_issued import BCServicesCardCredentialIssuedPage
from pageobjects.bc_wallet.information_sent_successfully import InformationSentSuccessfullyPage

class BCServicesCardReviewPage(BasePage):
    """BC Services Card Login with Username and Password page object"""

    # Locators
    on_this_page_text_locator = "Review"
    i_agree_locator = (AppiumBy.ACCESSIBILITY_ID, "I agree to the above terms")
    send_credential_locator = (AppiumBy.ACCESSIBILITY_ID, "Send Credential")


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_text_locator) 

    def i_agree(self):
        if self.on_this_page():
            #self.scroll_to_element(self.continue_locator[1])
            self.find_by(self.i_agree_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


    def send_credential(self):
        if self.on_this_page():
            self.find_by(self.send_credential_locator).click()
            #return BCServicesCardCredentialIssuedPage(self.driver)
            return InformationSentSuccessfullyPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
