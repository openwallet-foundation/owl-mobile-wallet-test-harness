from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage


# These classes can inherit from a BasePage to do common setup and functions
class OnboardingPrivateConfidentialPage(BasePage):
    """Onboarding Private and Confidential Screen page object"""

    # Locators
    on_this_page_text_locator = "Private and confidential"
    on_this_page_locator = (AppiumBy.NAME, "Private and confidential")
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    get_started_locator = (AppiumBy.ID, "com.ariesbifold:id/GetStarted")

    def on_this_page(self):
        if self.current_platform.lower() == "Android".lower():
            return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.on_this_page_locator)

    def get_onboarding_text(self):
        if self.on_this_page():
            pass
        else:
            raise Exception(f"App not on the {type(self)} page")


    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.bc_wallet.onboarding_digital_credentials import OnboardingDigitalCredentialsPage
            return OnboardingDigitalCredentialsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_get_started(self):
        if self.on_this_page():
            self.find_by(self.get_started_locator).click()
            return TermsAndConditionsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
