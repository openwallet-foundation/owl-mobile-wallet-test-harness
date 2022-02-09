from pageobjects.basepage import BasePage


class touchIDBiometrics(BasePage):
    """
    Figma:
        Category: Onboarding
        Sub Section: Touch ID Biometrics
        status: WIP
    """

    # locators
    continueBtnLocator: str = "00000000-0000-0008-ffff-ffff0000002c"
    backBtnLocator: str = "00000000-0000-0008-ffff-ffff000000b7"
    titleLocator: str = "Confirm your biometrics"
    # link 

    changeSecuritySettings: str = ""
    
    def rightPage(self) -> bool | None:
        if self.on_the_right_page(self.titleLocator):
            return True
        else:
            raise Exception("Not on the terms of service page")
    
    def selectContinueBtn(self) -> bool | None:
        if self.rightPage():
            self.find_by_element_id(self.continueBtnLocator).click()
            return True

    def selectBackBtn(self) -> bool | None:
        if self.rightPage():
            self.find_by_element_id(self.continueBtnLocator).click()
            return Truel

