import os
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.qc_wallet.onboardingstorecredssecurely import \
    OnboardingStoreCredsSecurelyPageQC
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingWelcomePageQC(BasePage):
    """Onboarding Welcome Screen QC page object"""

    on_this_page_text_locator = "Welcome"
    on_this_page_locator = (AppiumBy.NAME, "Welcome to the Quebec wallet")
    skip_locator = (AppiumBy.ID, "com.ariesbifold:id/Skip")
    next_locator = (AppiumBy.ID, "com.ariesbifold:id/Next")

    def on_this_page(self):
        language = self.get_app_language()
        if language == "English":
            self.on_this_page_text_locator = "Welcome to the Quebec wallet"
            self.on_this_page_locator = (AppiumBy.NAME, "Welcome to the Quebec wallet")
        else:
            self.on_this_page_text_locator = (
                "Bienvenue dans le portefeuille numérique du Québec"
            )
            self.on_this_page_locator = (
                AppiumBy.NAME,
                "Bienvenue dans le portefeuille numérique du Québec",
            )
        # Sometimes (especially when running with a local emulator ) where the app is not loaded yet.
        # Appium doesn't seem to let this happen when using Sauce Labs.
        timeout = 10
        if "Local" in os.environ["DEVICE_CLOUD"]:
            timeout = 100
        if self.current_platform.lower() == "Android".lower():
            return super().on_this_page(self.on_this_page_text_locator, timeout)
        return super().on_this_page(self.on_this_page_locator, timeout)

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
