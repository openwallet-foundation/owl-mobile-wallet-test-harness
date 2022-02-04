import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage

class explainerScreens(BasePage):
    """ Figma: 
            Category: Onboarding
            Sub Section: Explainer
            status: WIP

    """
    # Locators
    getStartedLocator: str = "00000000-0000-0020-ffff-ffff00000062" # WARN: cannot find the accessibility name
    nextBtnLocator: str = 'Next'
    backBtnLocator:str = 'Back'


    def selectGetStartedBtn(self) -> None:
        self.find_by_element_id(self.getStartedLocator).click()
        return

