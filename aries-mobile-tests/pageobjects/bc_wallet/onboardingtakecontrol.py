from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage

# These classes can inherit from a BasePage to do common setup and functions
class OnboardingTakeControlPage(BasePage):
    """Onboarding Take control of your information Screen page object"""

    # Locators
    # TODO: If Ontario/BC or other wallets are closely alligned and only locators are different, 
    # we could create a locator module that has all the locators. Given a specific app we could load the locators for that app. 
    # not sure this would be a use case that would be common. Leaving locators with the page objects for now.
    on_this_page_text_locator = "Privacy and confidentiality"
    on_this_page_locator = (AppiumBy.NAME, "Privacy and confidentiality")
    #learn_more_locator = "Learn more about BC Wallet"
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    get_started_locator = (AppiumBy.ID, "com.ariesbifold:id/GetStarted")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_locator)

    def get_onboarding_text(self):
        if self.on_this_page():
            pass
        else:
            raise Exception(f"App not on the {type(self)} page")

    # def select_learn_more(self):
    #     if self.on_this_page():
    #         self.find_by_accessibility_id(self.learn_more_locator).click()
    #         # TODO not sure what to do here if it opens a browser. return true for now.
    #         return True
    #     else:
    #         raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.bc_wallet.onboardingsharenecessary import OnboardingShareNecessaryPage
            return OnboardingShareNecessaryPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_get_started(self):
        if self.on_this_page():
            self.find_by(self.get_started_locator).click()
            return TermsAndConditionsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")