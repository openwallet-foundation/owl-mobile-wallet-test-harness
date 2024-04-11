from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.qc_wallet.onboardingtakecontrol import \
    OnboardingTakeControlPageQC
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingShareNecessaryPageQC(BasePage):
    """Onboarding Share only what is Necessary Screen page object"""

    on_this_page_text_locator = "Share only what is necessary"
    on_this_page_locator = (AppiumBy.NAME, "Share only what is necessary")
    skip_locator = (AppiumBy.ID, "com.ariesbifold:id/Skip")
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    next_locator = (AppiumBy.ID, "com.ariesbifold:id/Next")

    def on_this_page(self):
        if self.current_platform.lower() == "Android".lower():
            return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.on_this_page_locator)

    def select_next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            return OnboardingTakeControlPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.qc_wallet.onboardingstorecredssecurely import \
                OnboardingStoreCredsSecurelyPageQC

            return OnboardingStoreCredsSecurelyPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
