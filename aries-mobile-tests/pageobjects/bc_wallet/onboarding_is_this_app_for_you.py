from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboarding_a_different_smart_wallet import OnboardingADifferentSmartWalletPage
import os


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingIsThisAppForYouPage(BasePage):
    """Onboarding Is This App For You page object"""

    # Locators
    # TODO: If Ontario/BC or other wallets are closely alligned and only locators are different,
    # we could create a locator module that has all the locators. Given a specific app we could load the locators for that app.
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    on_this_page_text_locator = "Is this app for you?"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/DeveloperCounter")
    confirm_locator = (AppiumBy.ID, "com.ariesbifold:id/IAgree")
    continue_locator = (AppiumBy.ID, "com.ariesbifold:id/Continue")

    def on_this_page(self):
        # Sometimes (especially when running with a local emulator ) where the app is not loaded yet.
        # Appium doesn't seem to let this happen when using Sauce Labs.
        timeout = 10
        if "Local" in os.environ["DEVICE_CLOUD"]:
            timeout = 100
        if self.current_platform.lower() == "Android".lower():
            return super().on_this_page(self.on_this_page_text_locator, timeout)
        return super().on_this_page(self.on_this_page_locator, timeout)

    def get_onboarding_text(self):
        if self.on_this_page():
            pass
        else:
            raise Exception(f"App not on the {self.on_this_page_text_locator} page")

    def select_confirm(self):
        if self.on_this_page():
            self.find_by(self.confirm_locator).click()
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_continue(self):
        if self.on_this_page():
            self.find_by(self.continue_locator).click()
            return OnboardingADifferentSmartWalletPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
