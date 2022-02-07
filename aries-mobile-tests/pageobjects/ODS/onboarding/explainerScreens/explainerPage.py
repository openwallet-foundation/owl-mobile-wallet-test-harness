import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage

class explainerScreens(BasePage):
    """ 
    Figma: 
        Category: Onboarding
        Sub Section: Explainer Screens
        status: WIP
    """
    # Locators
    nextBtnLocator: str = 'Next'
    # backBtnLocator:str = 'Back' #BUG: undefined for now
    backBtnLocator: str = "00000000-0000-001d-ffff-ffff000000f6"
    skipBtnLocator: str = "00000000-0000-001d-ffff-ffff0000012c" # BUG: cannot find the accessibility name
    

    def selectSkipButton(self) -> None:
        self.find_by_element_id(self.skipBtnLocator).click()
        return 

    def selectNextBtn(self, index: int) -> int | None:
        self.find_by_element_id(self.nextBtnLocator).click()
        if index == 2:
            return None
        else: 
            index += 1 
            return index

    def selectBackBtn(self, index:int) -> int | None:
        self.find_by_element_id(self.backBtnLocator).click()
        if index == 0:
            return None
        else: 
            index -= 1
            return index



