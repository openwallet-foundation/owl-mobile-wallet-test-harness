from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.onboardingsharenecessary import OnboardingShareNecessaryPage
from pageobjects.qc_wallet.onboardingtakecontrol import OnboardingTakeControlPageQC
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingShareNecessaryPageQC(OnboardingShareNecessaryPage):
    """Onboarding Share only what is Necessary Screen page object"""

    on_this_page_text_locator = "Share only what is necessary"
    on_this_page_locator = (AppiumBy.NAME, "Share only what is necessary")

    def select_next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            return OnboardingTakeControlPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.qc_wallet.onboardingstorecredssecurely import (
                OnboardingStoreCredsSecurelyPageQC,
            )

            return OnboardingStoreCredsSecurelyPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
