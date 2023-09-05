from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage


class UpdatePINPage(PINSetupPage):
    """PIN Update page object"""

    # Locators
    on_this_page_text_locator = "Update your PIN"
    update_pin_button_locator = (
        AppiumBy.ID, "com.ariesbifold:id/UpdatePIN")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)


    def select_update_pin(self):
        if self.on_this_page():
            self.find_by(self.update_pin_button_locator).click()

            # Not sure what happens here yet
            #return OnboardingBiometricsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")