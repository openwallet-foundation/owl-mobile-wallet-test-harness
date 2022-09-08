from appium.webdriver.common.mobileby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do commone setup and functions
class CameraPrivacyPolicyPage(BasePage):
    """Camera Privacy Policy page object"""

    # Locators
    on_this_page_text_locator = "Privacy Policy"
    okay_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay")


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_okay(self):
        if self.on_this_page():
            self.find_by(self.okay_button_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")
