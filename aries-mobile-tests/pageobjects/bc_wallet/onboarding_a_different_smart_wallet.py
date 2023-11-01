from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboarding_digital_credentials import OnboardingDigitalCredentialsPage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage

# These classes can inherit from a BasePage to do common setup and functions
class OnboardingADifferentSmartWalletPage(BasePage):
    """Onboarding A Different Smart Wallet Screen page object"""

    # Locators
    on_this_page_text_locator = "A different smart wallet"
    on_this_page_locator = (AppiumBy.NAME, "A different smart wallet")
    skip_locator = (AppiumBy.ID, "com.ariesbifold:id/Skip")
    next_locator = (AppiumBy.ID, "com.ariesbifold:id/Next")

    def on_this_page(self):    
        if self.current_platform == "Android":
            return super().on_this_page(self.on_this_page_text_locator) 
        return super().on_this_page(self.on_this_page_locator)

    def get_onboarding_text(self):
        if self.on_this_page():
            pass
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            return OnboardingDigitalCredentialsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")