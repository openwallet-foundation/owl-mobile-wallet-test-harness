from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboardingtakecontrol import OnboardingTakeControlPage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage

# These classes can inherit from a BasePage to do common setup and functions
class OnboardingShareNecessaryPage(BasePage):
    """Onboarding Share only what is Necessary Screen page object"""

    # Locators
    # TODO: If Ontario/BC or other wallets are closely alligned and only locators are different, 
    # we could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    on_this_page_text_locator = "Receiving and using credentials"
    on_this_page_locator = (AppiumBy.NAME, "Receiving and using credentials")
    skip_locator = (AppiumBy.ID, "com.ariesbifold:id/Skip")
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    next_locator = (AppiumBy.ID, "com.ariesbifold:id/Next")

    def on_this_page(self):    
        return super().on_this_page(self.on_this_page_locator)

    def get_onboarding_text(self):
        if self.on_this_page():
            pass
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_next(self):
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            return OnboardingTakeControlPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.bc_wallet.onboardingstorecredssecurely import OnboardingStoreCredsSecurelyPage
            return OnboardingStoreCredsSecurelyPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")