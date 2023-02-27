from appium.webdriver.common.mobileby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition


# These classes can inherit from a BasePage to do commone setup and functions
class CameraPrivacyPolicyPage(BasePage):
    """Camera Privacy Policy page object"""

    # Locators
    on_this_page_text_locator = "Allow camera use"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/AllowCameraUse")
    #allow_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Allow")
    allow_button_locator = (AppiumBy.ACCESSIBILITY_ID, "Allow")
    not_now_button_locator = (AppiumBy.ID, "com.ariesbifold:id/NotNow")
    system_allow_while_using_app =  (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")


    def on_this_page(self):    
        #return super().on_this_page(self.on_this_page_locator) 
        #return super().on_this_page(self.allow_button_locator)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_not_now(self):
        self.find_by(self.not_now_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        return True

    def select_okay(self):
        self.find_by(self.allow_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        if self.driver.capabilities['platformName'] == 'Android':
            self.select_system_allow_while_using_app()
        return True

    def select_system_allow_while_using_app(self):
        self.find_by(self.system_allow_while_using_app, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
