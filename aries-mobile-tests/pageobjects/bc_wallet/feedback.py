import os
from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage

class FeedbackPage(BasePage):
    """Create a Give Feedback web(internal to the app) page object"""

    # Locators
    on_this_page_text_locator = "Give Feedback"
    next_locator = (AppiumBy.ACCESSIBILITY_ID, "Next")
    #exit_locator = (AppiumBy.ACCESSIBILITY_ID, "EXIT")
    #exit_locator = (AppiumBy.XPATH, "//a[normalize-space()='EXIT']")
    #exit_locator = (AppiumBy.XPATH, "//[contains('EXIT')]")
    #(AppiumBy.XPATH, "//[contains('XCUIElementTypeTextField')]")
    exit_locator = (AppiumBy.XPATH, "(//a[normalize-space()='EXIT'])[1]")


    def on_this_page(self):   
        return super().on_this_page(self.on_this_page_text_locator)  


    def select_next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            # pass for now, no need to text Survey Monkey
            pass
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_exit(self):
        if self.on_this_page():
            self.find_by(self.exit_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
