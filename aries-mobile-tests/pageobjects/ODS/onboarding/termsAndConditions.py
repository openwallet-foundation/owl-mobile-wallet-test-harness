import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


class explainerPages(BasePage):
    """
    Figma:
        Category: Onboarding
        Sub Section: Explainer Screens
        status: WIP
    """

    # Locators
    privacyStatementLinkLocator: str = ""  # INFO: no link?
    termsOfUsageLinkLocator: str = ""
    cehckboxTOSLocator: str = "I Agree to the Terms of Service"
    continueBtnLocator: str = "Continue"
    backBtnLocator: str = "Back"
    titleLocator: str = "Terms of Use"

    # INFO: test for swipping too?
    def rightPage(self) -> bool | None:
        if self.on_the_right_page(self.titleLocator):
            return True
        else:
            raise Exception("Not on the terms of service page")

    def selectConitnueBtn(self) -> None:
        if self.rightPage:
            self.find_by_accessibility_id(self.continueBtnLocator).click()
            return

    def selectBackBtn(self) -> None:
        if self.rightPage:
            self.find_by_accessibility_id(self.continueBtnLocator).click()
            return

    def selectBackBtn(self, index: int) -> int | None:
        self.find_by_element_id(self.backBtnLocator).click()
        if index == 0:
            return None
        else:
            index -= 1
            return index
