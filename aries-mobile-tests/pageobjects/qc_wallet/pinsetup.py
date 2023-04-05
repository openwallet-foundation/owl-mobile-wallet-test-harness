from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.onboarding_biometrics import OnboardingBiometricsPage
from pageobjects.bc_wallet.pinsetup import PINSetupPage


class PINSetupPageQC(PINSetupPage):
    """PIN Setup page QC object"""

    # Locators
    first_pin_visibility_locator = (
        AppiumBy.ID, "com.ariesbifold:id/Show")
    second_pin_visibility_locator = (
        AppiumBy.ID, "com.ariesbifold:id/Show")


    def __init__(self, driver):
        super().__init__(driver)
    
    def get_pin(self):
        if self.on_this_page():
            # PIN must be visable.
            self.find_by(self.first_pin_visibility_locator).click()
            return self.find_by(self.first_pin_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_second_pin(self):
        if self.on_this_page():
            # PIN must be visable.
            self.find_by(self.second_pin_visibility_locator).click()
            return self.find_by(self.second_pin_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")
    
    def create_pin(self):
        if self.on_this_page():
            self.find_by(self.create_pin_button_tid_locator).click()

            if self.find_by(self.modal_message_ok_locator).is_displayed():
                return PINSetupPageQC(self.driver)
            # return the wallet initialization page
            return OnboardingBiometricsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
