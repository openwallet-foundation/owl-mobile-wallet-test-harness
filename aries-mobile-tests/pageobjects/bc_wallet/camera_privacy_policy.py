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
    allow_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Allow")
    #allow_button_locator = (AppiumBy.ACCESSIBILITY_ID, "Allow")
    not_now_button_locator = (AppiumBy.ID, "com.ariesbifold:id/NotNow")
    system_allow_while_using_app =  (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")


    def on_this_page(self):    
        # 8 sec
        return super().on_this_page(self.on_this_page_locator) 
        # 14 sec
        #return super().on_this_page(self.allow_button_locator, timeout=5)
        # 19 sec
        return super().on_this_page(self.on_this_page_text_locator)

    def select_not_now(self):
        self.find_by(self.not_now_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        #self.find_by(self.not_now_button_locator, wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED).click()
        # 26 sec
        #self.find_by(self.not_now_button_locator, wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED).click()
        return True

    def select_allow(self):
        # 26 sec
        #self.find_by(self.allow_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        # 19 sec
        self.find_by(self.allow_button_locator, wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED).click()
        # 28 sec
        #self.find_by(self.allow_button_locator, wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED).click()
        # 22 sec
        #self.find_by((AppiumBy.ACCESSIBILITY_ID, "Allow"), wait_condition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED).click()
        if self.driver.capabilities['platformName'] == 'Android':
            self.select_system_allow_while_using_app()
        return True

    def select_system_allow_while_using_app(self):
        self.find_by(self.system_allow_while_using_app, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
