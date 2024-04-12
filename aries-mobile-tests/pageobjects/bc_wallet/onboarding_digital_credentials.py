from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboarding_private_confidential import OnboardingPrivateConfidentialPage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage

# These classes can inherit from a BasePage to do common setup and functions
class OnboardingDigitalCredentialsPage(BasePage):
    """Onboarding Digital Credentials Screen page object"""

    # Locators
    on_this_page_text_locator = "Digital credentials"
    on_this_page_locator = (AppiumBy.NAME, "Digital credentials")
    #skip_locator = (AppiumBy.ID, "com.ariesbifold:id/Skip")
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
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
            return OnboardingPrivateConfidentialPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.bc_wallet.onboarding_a_different_smart_wallet import OnboardingADifferentSmartWalletPage
            return OnboardingADifferentSmartWalletPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    # def select_skip(self):
    #     if self.on_this_page():
    #         self.find_by(self.skip_locator).click()
    #         return TermsAndConditionsPage(self.driver)
    #     else:
    #         raise Exception(f"App not on the {type(self)} page")