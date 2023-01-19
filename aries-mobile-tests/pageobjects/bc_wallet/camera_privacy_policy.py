from appium.webdriver.common.mobileby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do commone setup and functions
class CameraPrivacyPolicyPage(BasePage):
    """Camera Privacy Policy page object"""

    # Locators
    on_this_page_text_locator = "Allow camera use"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/AllowCameraUse")
    allow_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Allow")
    not_now_button_locator = (AppiumBy.ID, "com.ariesbifold:id/NotNow")


    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_locator) 

    def select_not_now(self):
        if self.on_this_page():
            self.find_by(self.not_now_button_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_okay(self):
        if self.on_this_page():
            self.find_by(self.allow_button_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")
