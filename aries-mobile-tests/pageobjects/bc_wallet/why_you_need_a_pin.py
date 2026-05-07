from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage

# These classes can inherit from a BasePage to do commone setup and functions
class WhyYouNeedAPINPage(BasePage):
    """Secure your wallet Why you need a PIN Info page object"""

    # Locators
    on_this_page_text_locator = "Create a PIN"
    on_this_page_locator = (AppiumBy.NAME, "Create a PIN")
    continue_locator = (
        AppiumBy.ID, "com.ariesbifold:id/ContinueCreatePIN")

    def on_this_page(self):   
        if self.current_platform == "Android":
            return super().on_this_page(self.on_this_page_text_locator)  
        return super().on_this_page(self.on_this_page_locator) 

    def select_continue(self):
        # Remove the platform check when BC Wallet bug 2264 is fixed
        if self.current_platform == "Android":
            self.scroll_to_bottom()
        self.find_by(self.continue_locator).click()

        # return the wallet biometrics page
        return PINSetupPage(self.driver)