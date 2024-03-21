from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from time import sleep


# These classes can inherit from a BasePage to do commone setup and functions
class TermsAndConditionsPage(BasePage):
    """Terms and Conditions page object"""

    # Locators
    on_this_page_text_locator = "Terms of Use"
    on_this_page_locator = (AppiumBy.NAME, "Terms of Use")
    accept_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Accept")
    accept_button_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Accept")


    def on_this_page(self):       
        if self.current_platform == "Android":
            return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.on_this_page_locator) 

    def select_accept(self):
        if self.on_this_page():
            # As of 2024-03-21 the app no longer needs to scroll to get to the accept button. BC Wallet Build 1603
            # Leaving this code here just in case it is needed in the future, and for reference on scrolling.
            # try:
            #     self.scroll_to_element(self.back_aid_locator[1])
            # except:
            #     # Sometimes it seems that scrolling may try to access the element by accessibility id before it appears
            #     # if we get this failure then just sleep and try again. 
            #     sleep(5)
            #     self.scroll_to_element(self.back_aid_locator[1])
            self.find_by(self.accept_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return PINSetupPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
