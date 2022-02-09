from pageobjects.basepage import BasePage


class initialOnboarding(BasePage):

    """
    Figma:
        Category: Onboarding
        Sub Section: Explainer Screens
        status: WIP
    """

    # Locators
    getStartedLocator: str = "00000000-0000-0017-ffff-ffff0000009d"  # BUG: cannot find the accessibility name
    securitySettingsLocator: str = "00000000-0000-001d-ffff-ffff0000002b"
    # BUG: cannot find the accessibility name
    titleLocator: str = "00000000-0000-001d-ffff-ffff00000025"  
    # WARN: no accessibility name but is it required?

    def rightPage(self) -> bool | None:
        if self.on_the_right_page(self.titleLocator):
            return True
        else:
            raise Exception("Not on the terms of service page")

    def selectSecuritySettings(self) ->  bool | None:
        if self.rightPage():
            self.find_by_element_id(self.securitySettingsLocator).click()
            return True

    def selectGetStartedBtn(self) -> bool | None:
        if self.rightPage():
            self.find_by_element_id(self.getStartedLocator).click()
            return True
