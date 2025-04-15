from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.bc_wallet.pinsetup import PINSetupPage


# These classes can inherit from a BasePage to do commone setup and functions
class PinExplainerPage(BasePage):
    """Pin Explainer page object"""

    # Locators
    on_this_page_text_locator = "Create a PIN"
    on_this_page_locator = (AppiumBy.NAME, "Create a PIN")
    continue_button_locator = (AppiumBy.ID, "com.ariesbifold:id/ContinueCreatePIN")
    continue_button_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Global.Continue")


    def on_this_page(self):       
        if self.current_platform == "Android":
            return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.on_this_page_locator) 

    def select_continue(self):
        if self.on_this_page():
            self.find_by(self.continue_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return PINSetupPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
