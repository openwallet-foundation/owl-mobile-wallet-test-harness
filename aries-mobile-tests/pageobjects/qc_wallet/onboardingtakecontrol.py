from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.onboardingtakecontrol import OnboardingTakeControlPage
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingTakeControlPageQC(OnboardingTakeControlPage):
    """Onboarding Take control of your information Screen QC page object"""

    on_this_page_text_locator = "Take control of your information"
    on_this_page_locator = (AppiumBy.NAME, "Take control of your information")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.qc_wallet.onboardingsharenecessary import (
                OnboardingShareNecessaryPageQC,
            )

            return OnboardingShareNecessaryPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_get_started(self):
        if self.on_this_page():
            self.find_by(self.get_started_locator).click()
            return TermsAndConditionsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
