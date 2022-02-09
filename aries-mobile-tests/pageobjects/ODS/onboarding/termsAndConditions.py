from typing import Union

from pageobjects.basepage import BasePage


class termsAndConditions(BasePage):
    """
    Figma:
        Category: Onboarding
        Sub Section: Explainer Screens
        status: WIP
    """

    # Locators
    privacyStatementLinkLocator: str = ""  # INFO: no link?
    termsOfUsageLinkLocator: str = ""
    checkboxTOSLocator: str = "I Agree to the Terms of Service"
    continueBtnLocator: str = "Continue"
    backBtnLocator: str = "Back"
    titleLocator: str = "Terms of Use"

    # INFO: test for swipping too?
    def rightPage(self) -> Union[bool,None]:
        if self.on_the_right_page(self.titleLocator):
            return True
        else:
            raise Exception("Not on the terms of service page")

    def selectContinueBtn(self) -> None:
        if self.rightPage():
            self.find_by_accessibility_id(self.continueBtnLocator).click()
            return

    def selectBackBtn(self) -> None:
        if self.rightPage():
            self.find_by_accessibility_id(self.continueBtnLocator).click()
            return
    
    def checkTOSBox(self) -> None:
        if self.rightPage():
            self.find_by_accessibility_id(self.checkboxTOSLocator)


