from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.onboardingstorecredssecurely import (
    OnboardingStoreCredsSecurelyPage,
)
from pageobjects.qc_wallet.onboardingsharenecessary import (
    OnboardingShareNecessaryPageQC,
)
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC


class OnboardingStoreCredsSecurelyPageQC(OnboardingStoreCredsSecurelyPage):
    """Onboarding Store your Credentials Securely Screen page object"""

    on_this_page_text_locator = "A digital credential"
    on_this_page_locator = (AppiumBy.NAME, "A digital credential, secretly saved")

    def select_next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            return OnboardingShareNecessaryPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.qc_wallet.onboardingwelcome import OnboardingWelcomePageQC

            return OnboardingWelcomePageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
