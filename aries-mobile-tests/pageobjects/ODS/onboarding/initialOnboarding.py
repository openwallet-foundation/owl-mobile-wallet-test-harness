import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage

class initialOnboarding(BasePage):
    """ 
    Figma: 
        Category: Onboarding
        Sub Section: Explainer Screens
        status: WIP
    """
    # Locators
    getStartedLocator: str = "00000000-0000-0017-ffff-ffff0000009d" # BUG: cannot find the accessibility name
    securitySettingsLocator: str = "00000000-0000-001d-ffff-ffff0000002b" # BUG: cannot find the accessibility name
    titleLocator: str = "00000000-0000-001d-ffff-ffff00000025" # WARN: no accessibility name but is it required?


    def selectSecuritySettings(self) -> None | bool:
        if self.on_the_right_page(self.titleLocator):
            self.find_by_element_id(self.securitySettingsLocator).click()
            return
        else:
             raise Exception(f"App not on the {self.titleLocator} page")
      
        #00000000-0000-0024-ffff-ffff000002b2


    def selectGetStartedBtn(self) -> bool:
        if self.on_the_right_page(self.titleLocator):
            self.find_by_element_id(self.getStartedLocator).click()
            return True
        else: 
            #WARN: the QA dev is relative new
            raise Exception(f"App not on the {self.titleLocator} page")
