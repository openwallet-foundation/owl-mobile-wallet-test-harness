from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
#from pageobjects.bc_wallet.bc_services_card_login_vt_pc import BCServicesCardLoginVTPCPage

class BCServicesCardLoginVTPCPage(BasePage):
    """BC Services Card Login Virtual Testing passcode Entry page object"""

    # Locators
    on_this_page_text_locator = "Passcode"
    passcode_locator = (AppiumBy.ACCESSIBILITY_ID, "Passcode")
    continue_locator = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator, 50) 

    def enter_passcode(self, csn):
        if self.on_this_page():
            self.find_by(self.passcode_locator).send_keys(csn)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_continue(self):
        if self.on_this_page():
            self.find_by(self.continue_locator).click()

            # return the passcode entry page
            #return BCServicesCardLoginVTPCPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page") 
