from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.onboardingwelcome import OnboardingWelcomePage
from pageobjects.qc_wallet.onboardingstorecredssecurely import (
    OnboardingStoreCredsSecurelyPageQC,
)
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingWelcomePageQC(OnboardingWelcomePage):
    """Onboarding Welcome Screen QC page object"""

    on_this_page_locator = (AppiumBy.NAME, "Welcome to the Quebec wallet")

    def select_next(self):
        if self.on_this_page():
            try:
                self.find_by(self.next_locator).click()
            except:
                print("Element not found. Waiting 10 seconds and trying again...")
                sleep(10)
                self.find_by(self.next_locator).click()
            return OnboardingStoreCredsSecurelyPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
