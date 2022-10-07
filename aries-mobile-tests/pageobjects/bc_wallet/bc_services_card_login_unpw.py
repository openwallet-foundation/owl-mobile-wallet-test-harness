from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.bc_services_card_review import BCServicesCardReviewPage

class BCServicesCardLoginUNPWPage(BasePage):
    """BC Services Card Login with Username and Password page object"""

    # Locators
    on_this_page_text_locator = "Email or username"
    username_locator = (AppiumBy.ACCESSIBILITY_ID, "Email or username")
    #username_locator = (AppiumBy.CLASS_NAME, "XCUIElementTypeTextField")
    #(AppiumBy.XPATH, "//[contains('XCUIElementTypeTextField')]")
    password_locator = (AppiumBy.ACCESSIBILITY_ID, "Password")
    #password_locator = (AppiumBy.CLASS_NAME, "XCUIElementTypeSecureTextField")
    continue_locator = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator, 50) 

    def enter_username(self, username):
        if self.on_this_page():
            self.find_by(self.username_locator).send_keys(username)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_password(self, password):
        if self.on_this_page():
            self.find_by(self.password_locator).send_keys(password)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_continue(self):
        if self.on_this_page():
            self.find_by(self.continue_locator).click()

            # return the BC Services Card Card Account Review Credential details page
            return BCServicesCardReviewPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page") 
